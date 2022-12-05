# dbus-mqtt-services
A [driver](https://github.com/victronenergy/venus/wiki/howto-add-a-driver-to-Venus) 
for [VenusOS](https://github.com/victronenergy/venus/wiki), which listens on a special 
MQTT and creates a new "service" on the dbus as instructed in the MQTT-message. This allows 
you to create whatever service you desire on the dbus without having to run special 
python-code on the VenusOS device.

Credits: Louis Van Der Walt's [dbus-serialbattery](https://github.com/Louisvdw/dbus-serialbattery)
was a great inspiration for this work.

## Example
The following example message published to the topic `W/dbus-mqtt-services` will generate a 
new battery service on the dbus:

    {
      "service": "daly_bms_battery_1",
      "serviceType": "battery",
      "serviceInstance": 0,
      "dbus_data": [
        {
          "path": "/Mgmt/ProcessName",
          "value": "Daly Bms Bridge",
          "valueType": "string",
          "writeable": false
        },
        {
          "path": "/Mgmt/ProcessVersion",
          "value": "1.0",
          "valueType": "string",
          "writeable": false
        },
        {
          "path": "/Mgmt/Connection",
          "value": "Serial Uart Daly",
          "valueType": "string",
          "writeable": false
        },
        {
          "path": "/ProductId",
          "value": "0",
          "valueType": "integer",
          "writeable": false
        },
        {
          "path": "/ProductName",
          "value": "Daly Bms service",
          "valueType": "string",
          "writeable": false
        },
        {
          "path": "/FirmwareVersion",
          "value": "1.0",
          "valueType": "string",
          "writeable": false
        },
        {
          "path": "/HardwareVersion",
          "value": "1.0",
          "valueType": "string",
          "writeable": false
        },
        {
          "path": "/Connected",
          "value": "1",
          "valueType": "integer",
          "writeable": false
        },
        {
          "path": "/CustomName",
          "value": "Daly Bms service",
          "valueType": "string",
          "writeable": true
        },
        {
          "path": "/Info/BatteryLowVoltage",
          "value": "52.176",
          "valueType": "float",
          "writeable": false
        },
      ]
    }

## Install
The installation procedure requires [SSH root access](https://www.victronenergy.com/live/ccgx:root_access) to your VenusOS device.

    $ wget https://raw.githubusercontent.com/sebdehne/dbus-mqtt-services/master/etc/dbus-mqtt-services/installrelease.sh
    $ sh installrelease.sh
    $ reboot

## How to remove settings from 'localsettings'
In case your service creates an vrm-instance which you do not want, here is how to remove settings:

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

