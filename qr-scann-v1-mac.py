#!/usr/bin/python
# -*- coding: utf-8 -*-
# Read the serial port and write the output to the screen,
# simulate keyboard presses (using crikey)
# Written by Romain Aviolat 05.2012
# adopted for macOs by oliver steiner 06.2018
# requirements: pip3 install pyserial

import os, sys, argparse
import serial

class handscanner:
    def __init__(self):
        self.port = ''
        self.portSpeed = '9600'
    #    self.crikey = '/usr/local/bin/crikey'
        self.errorMsg = ""
        self.trailer = '0d'

    def checkDependencies(self):

        if os.path.exists(self.port):
            return True
        else:
            self.errorMsg = "scanner not connected on " + self.port

            print(self.errorMsg)
            return False

    def readData(self, source=None, event=None):

        ser = serial.Serial(self.port, self.portSpeed)

        while 1 != 0:

            charHex = ""
            barcode = ""

            while charHex != self.trailer:
              #  char = ser.read(1)
                char = '0'
                charHex = char.encode('hex')
                barcode = barcode + char

        ##    cmd = self.crikey + " " + barcode
            cmd = barcode
            os.system(cmd)


if __name__ == '__main__':

    device = handscanner()

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', help="Specify the device ex: /dev/rfcomm0")
    parser.add_argument('-D', '--daemon', action="store_true", help="Fork and run in background")
    args = parser.parse_args()

    if args.device:
        device.port = args.device

    else:
      #  device.port = '1'
        device.port = '/dev/cu.Bluetooth-Incoming-Port'  # macOS 10.13
      #  device.port = '/dev/tty.Bluetooth-Incoming-Port'  # macOS 10.13
        print("no port specified, trying Bluetooth-Incoming-Port, more info: -h (help)")
       # sys.exit(0)

    if device.checkDependencies() is True:

        if args.daemon:

            if os.fork() == 0:
                os.setsid()
                sys.stdout = open("/dev/null", 'w')
                sys.stdin = open("/dev/null", 'r')

                if os.fork() == 0:
                    device.readData()
                sys.exit(0)

        else:
            print(device)
            device.readData()