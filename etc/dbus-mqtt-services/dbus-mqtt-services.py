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

# Victron packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '/opt/victronenergy/dbus-systemcalc-py/ext/velib_python'))
from settingsdevice import SettingsDevice
from vedbus import VeDbusService


def get_bus():
    return dbus.SessionBus() if 'DBUS_SESSION_BUS_ADDRESS' in os.environ else dbus.SystemBus()


client = mqtt.Client(client_id="")
topic = "W/dbus-mqtt-services"

known_dbus_services = {}


class DbusService:
    def __init__(self, dbus_service, dbus_service_type, dbus_service_instance, dbus_data):
        self.dbus_service = dbus_service
        self.dbus_service_type = dbus_service_type
        self.dbus_service_instance = dbus_service_instance

        # Find an existing VRM-instance ID in "localsettings", or add it as needed:
        settings_device = SettingsDevice(get_bus(), {}, eventCallback=None)
        busitem = settings_device.addSetting(
            '/Settings/Devices/' + dbus_service + '/ClassAndVrmInstance',
            dbus_service_type + ':' + str(dbus_service_instance),
            0,
            0
        )
        val = busitem.get_value().split(':')
        self.dbus_service_type = val[0]
        self.dbus_service_instance = int(val[1])
        print("New service added: ", self.dbus_service, self.dbus_service_type, ":" + str(self.dbus_service_instance))

        # start Dbus-service
        self.dbusservice = VeDbusService("com.victronenergy." + dbus_service_type + "." + dbus_service, get_bus())
        self.dbusservice.add_path("/DeviceInstance", self.dbus_service_instance)

        # add all paths for our service:
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
            try:
                self.dbusservice.add_path(path, value, writeable=writeable)
            except KeyError:
                print("Could not add path " + path)


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

            # print("Updated " + path + " " + str(value))
            try:
                self.dbusservice[path] = value
            except KeyError:
                print("Could not update path " + path)


def main():
    global client
    global topic

    client.on_message = on_message
    client.connect("127.0.0.1")
    client.subscribe(topic)
    client.loop_start()

    mainloop = gobject.MainLoop()
    DBusGMainLoop(set_as_default=True)

    print("==== dbus-mqtt-services started ====")

    try:
        mainloop.run()
    except KeyboardInterrupt:
        pass


def on_message(client, userdata, message):
    global known_dbus_services
    payload = str(message.payload.decode("utf-8"))
    json_data = json.loads(payload)

    # print("message received ", payload)
    # print("message jsonData ", json_data)
    # print("message topic=", message.topic)
    # print("message qos=", message.qos)
    # print("message retain flag=", message.retain)

    service = json_data["service"]
    dbus_data = json_data["dbus_data"]
    if service in known_dbus_services:
        try:
            known_dbus_services[service].republish(dbus_data)
        except Exception as e:
            print("Could not update service:")
            print(e)

    else:
        service_type = json_data["serviceType"]
        service_instance = json_data["serviceInstance"]
        try:
            known_dbus_services[service] = DbusService(service, service_type, service_instance, dbus_data)
        except Exception as e:
            print("Could not add new service:")
            print(e)


if __name__ == "__main__":
    main()
