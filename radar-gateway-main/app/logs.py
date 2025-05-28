#! /usr/bin/python
import ntplib
from datetime import datetime, timezone
import gui_parser as parser
from time import sleep
import sys


read_T = float(sys.argv[1])
usb = sys.argv[2]


def reset(T, com):
    # Sleep and send anything in TX to reset the device
    com.sendByte(0xff)
    sleep(T)
    com.sendByte(0xff)


if __name__ == '__main__':
    # Opening COM port and connecting to broker
    comPort = parser.UARTParser("DoubleCOMPort")
    comPort.connectDataComPort(usb)
    reset(read_T, comPort)
    # Start loop for logging
    while(True):
        # Reading COM port and log it with Parser
        parsed, raw = comPort.logParsing()
        # Print timestamp
        print("datetime:", datetime.fromtimestamp(datetime.now(timezone.utc).timestamp()))
        # Print raw data
        # print(raw)
        # Print parsed data
        print(parsed)
        # Sleep
        sleep(read_T)
