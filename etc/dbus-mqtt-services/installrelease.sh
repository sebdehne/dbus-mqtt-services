#!/bin/sh
curl -s https://api.github.com/repos/sebdehne/dbus-mqtt-services/releases/latest | grep "browser_download_url.*gz" | cut -d : -f 2,3 | tr -d \" | wget -O venus-data.tar.gz -qi -
tar -zxf ./venus-data.tar.gz -C /data
sh /data/etc/dbus-mqtt-services/reinstalllocal.sh
