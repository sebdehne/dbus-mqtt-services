#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys

import dbus
import paho.mqtt.client as mqtt
# Dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib as gobject

DBusGMainLoop(set_as_default=True)

# Victron packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '/opt/victronenergy/dbus-systemcalc-py/ext/velib_python'))
from settingsdevice import SettingsDevice
from vedbus import VeDbusService


def get_bus():
    return dbus.SessionBus() if 'DBUS_SESSION_BUS_ADDRESS' in os.environ else dbus.SystemBus()


client = mqtt.Client(client_id="")
topic = "/dbus-mqtt-services"

known_dbus_services = {}


class DbusService:
    def __init__(self, dbus_service, dbus_service_type, dbus_service_instance, dbus_data):
        self.dbus_service = dbus_service
        self.dbus_service_type = dbus_service_type
        self.dbus_service_instance = dbus_service_instance

        settings = {
            'instance': [
                '/Settings/Devices/' + dbus_service + '/ClassAndVrmInstance',
                [dbus_service_type + ':' + str(dbus_service_instance)],
                0,
                0
            ],
        }

        settings_device = SettingsDevice(get_bus(), settings, eventCallback=None)
        val = settings_device['instance'].split(':')
        self.dbus_service_type = val[0]
        self.dbus_service_instance = int(val[1])
        print("new service added: ", self.dbus_service, self.dbus_service_type, ":" + str(self.dbus_service_instance))

        self.dbusservice = VeDbusService("com.victronenergy." + dbus_service_type + "." + dbus_service, get_bus())
        self.dbusservice.add_path("/DeviceInstance", self.dbus_service_instance)

        for dbus_item in dbus_data:
            path = dbus_item["path"]
            writeable = dbus_item["writeable"]
            value = dbus_item["value"]
            value_type = dbus_item["valueType"]

            if value_type == "integer":
                value = int(value)
            elif value_type == "float":
                value = float(value)
            elif value_type == "none":
                value = None

            print("Add path " + path + " " + str(value))
            self.dbusservice.add_path(path, value, writeable=writeable)

    def republish(self, dbus_data):

        for dbus_item in dbus_data:
            path = dbus_item["path"]
            value = dbus_item["value"]
            value_type = dbus_item["valueType"]

            if value_type == "integer":
                value = int(value)
            elif value_type == "float":
                value = float(value)
            elif value_type == "none":
                value = None

            print("Updated " + path + " " + str(value))
            self.dbusservice[path] = value


def main():
    global client
    global topic

    client.on_message = on_message
    client.connect("192.168.1.18")
    client.subscribe("W" + topic)
    client.loop_start()

    mainloop = gobject.MainLoop()

    try:
        mainloop.run()
    except KeyboardInterrupt:
        pass


def on_message(client, userdata, message):
    global known_dbus_services
    payload = str(message.payload.decode("utf-8"))
    json_data = json.loads(payload)

    print("message received ", payload)
    print("message jsonData ", json_data)
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    service = json_data["service"]
    dbus_data = json_data["dbus_data"]
    if service in known_dbus_services:
        known_dbus_services[service].republish(dbus_data)
    else:
        service_type = json_data["serviceType"]
        service_instance = json_data["serviceInstance"]
        known_dbus_services[service] = DbusService(service, service_type, service_instance, dbus_data)


if __name__ == "__main__":
    main()
