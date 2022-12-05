#!/bin/sh

#handle read only mounts
sh /opt/victronenergy/swupdate-scripts/remount-rw.sh

chmod 777 /data/rc.local  &>/dev/null
chmod 777 /data/etc/dbus-mqtt-services/service/run  &>/dev/null
chmod 777 /data/etc/dbus-mqtt-services/service/log/run  &>/dev/null

ln -s /data/etc/dbus-mqtt-services /opt/victronenergy/dbus-mqtt-services &>/dev/null
ln -s /data/etc/dbus-mqtt-services/service /service/dbus-mqtt-services &>/dev/null

