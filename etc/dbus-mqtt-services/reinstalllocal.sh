#!/bin/sh

#handle read only mounts
sh /opt/victronenergy/swupdate-scripts/remount-rw.sh

ln -s /data/etc/dbus-mqtt-services /opt/victronenergy/dbus-mqtt-services &>/dev/null
ln -s /data/etc/dbus-mqtt-services /service/dbus-mqtt-services &>/dev/null

