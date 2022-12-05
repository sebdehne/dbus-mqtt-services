# dbus-mqtt-services
A driver for VenusOS, listens on a special MQTT and creates a new service in the dbus
as instructed in the MQTT-message. This allows you to create whatever service you desire
on the dbus without having to run special python-code on the VenusOS device.

## add InstanceID
    dbus -y com.victronenergy.settings /Settings/Devices AddSetting daly_bms_battery_1 ClassAndVrmInstance battery:0 s "" ""

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

