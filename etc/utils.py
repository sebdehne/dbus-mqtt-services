# -*- coding: utf-8 -*-
import logging
import serial
from time import sleep
from struct import *
import bisect

# Logging
logging.basicConfig()
logger = logging.getLogger("MqttBattery")
logger.setLevel(logging.INFO)

