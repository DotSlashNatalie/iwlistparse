#!/usr/bin/env python

"""
This is used to parse the output from iwlist scan
ie

iwlist wlan0 scan | python iwlistparse.py

Sample output:

7E:85:2A:A6:C0:D8 - 2.412 GHz (Channel 1) - 30/70  Signal level=-80 dBm - xfinitywifi
DC:EF:09:83:B9:E3 - 2.412 GHz (Channel 1) - 70/70  Signal level=-38 dBm - NETGEAR46

You can use the watch command to continuously run it -
watch -n 1 'iwlist wlan0 scan | python iwlistparse.py'

If you would like it to modified to be in a more consumable/queryable format (ie CSV or SQL)
please contact me
"""

__author__ = "Nathan Adams"
__copyright__ = "Copyright 2018, Nathan Adams"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Nathan Adams"
__email__ = "nathan[at]allostech.com"
__status__ = "Production"

import re
import sys

def re_match_1(reString, lines):
    for x in range(0, len(lines) - 1):
        match = re.match(reString, lines[x])
        if match:
            return match.group(1)
    return None

with sys.stdin as f:
    address = ""
    freq = ""
    signal = ""
    ssid = ""
    lines = f.readlines()
    i = 0
    while lines:
        #           Cell 01 - Address: 7E:85:2A:A6:C0:D8
        if i >= len(lines):
            break
        match = re.match("\s+Cell [0-9]{2} - Address: ([A-F\:0-9]+)", lines[i])
        if match:
            address = match.group(1)
            freq = re_match_1("\s+Frequency:(.*)", lines[i:])
            signal = re_match_1("\s+Quality=(.*)", lines[i:])
            ssid = re_match_1("\s+ESSID:\"(.*)\"", lines[i:])
            if not ssid:
                ssid = "<no ssid>"
            i = i + 3
            #lines = lines[i:]
            print "%s - %s - %s - %s" % (address, freq, signal, ssid)
        else:
            i = i + 1
