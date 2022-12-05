# dbus-mqtt-services
A driver for [VenusOS](https://github.com/victronenergy/venus/wiki), which listens on a special MQTT and creates a new service in the dbus
as instructed in the MQTT-message. This allows you to create whatever service you desire
on the dbus without having to run special python-code on the VenusOS device.

## Install
The installation procedure requires [SSH root access](https://www.victronenergy.com/live/ccgx:root_access) to your VenusOS device.

    $ /data/etc


## How to remove settings from 'localsettings'
    # stop the localsettings service
    $ svc -d /service/localsettings

    # make a backup
    $ cd /data/conf
    $ cp settings.xml settings.xml.backup

    # remove the settings as needed
    $ vi settings.xml

    # bring the localsettings service back online
    $ svc -u /service/localsettings
    
    # check the logs for any issues
    $ less /data/log/localsettings/current

