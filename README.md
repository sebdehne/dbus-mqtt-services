# dbus-mqtt-services
A driver for [VenusOS](https://github.com/victronenergy/venus/wiki), which listens on a special MQTT and creates a new service in the dbus
as instructed in the MQTT-message. This allows you to create whatever service you desire
on the dbus without having to run special python-code on the VenusOS device.

## Install
The installation procedure requires [SSH root access](https://www.victronenergy.com/live/ccgx:root_access) to your VenusOS device.

Download the code
    
    $ cd
    $ curl https://raw.githubusercontent.com/sebdehne/dbus-mqtt-services/master/dbus-mqtt-services.py -o dbus-mqtt-services.py

Create a symbolic link

    $ ln -s /data/etc/dbus-mqtt-services.py /opt/victronenergy/dbus-mqtt-services.py

## How to remove settings from 'localsettings'

Stop the localsettings service

    $ svc -d /service/localsettings

Make a backup

    $ cd /data/conf
    $ cp settings.xml settings.xml.backup

Remove the settings as needed

    $ vi settings.xml

Bring the localsettings service back online

    $ svc -u /service/localsettings
    
Check the logs for any issues

    $ less /data/log/localsettings/current

