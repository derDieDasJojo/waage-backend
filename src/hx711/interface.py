#! /usr/bin/python3

import time
import sys

EMULATE_HX711=False

#referenceUnit = 1
#referenceUnit = 9955

config = {
    "referenceUnit": 9955,
    "offset": 0
}


if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def get_default_config():
    return config

def init():
    setup()
    hx.tare(30)
    config.offset = hx.get_offset_A()
    print("Tare done! Add weight now...")
    return config

def setup(config=None):
    # get default config
    if config==None:
        config = get_default_config()
    # setup AD Converter
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(config.referenceUnit)
    hx.set_offset_A(config.offset)
    hx.reset()

def getWeight(config):
    setup(config)
    try:
        val = hx.get_weight(9)
        print("{0:.2f} kg".format(val))
        hx.power_down()
        hx.power_up()
        return val
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        hx.cleanup()
