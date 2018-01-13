#!/usr/bin/env python
# coding: latin-1

import ThunderBorg
import sys
import math

# Edit these
MIN_POWER = 10
MAX_POWER = 20

POWER_RANGE = float(MAX_POWER - MIN_POWER)

class MotorChannel(object):
    def __init__(self, tb, index, channel):
        self._tb = tb
        self._index = index
        self._channel= channel
        self._power = 0

    # Not yet fully implemented
    def percentToPower(percent):
        p = math.abs(percent)
        power = (((float(p) / 100.0) * POWER_RANGE) + MIN_POWER) / 100.0
        if percent < 0:
            power = -power
        return power

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value
        print 'Setting motor', self._channel, "to", value, "%"
        if self._channel == 0:
            self._tb.SetMotor1(float(value) / 100.0)
        else:
            self._tb.SetMotor2(float(value) / 100.0)


class Motor(object):
    def __init__(self, tb, index):
        self.m0 = MotorChannel(tb, index, 0)
        self.m1 = MotorChannel(tb, index, 1)


class Robot(object):
    def __init__(self):
        self._tb = ThunderBorg.ThunderBorg()
        self._tb.Init()

        if not self._tb.foundChip:
            boards = ThunderBorg.ScanForThunderBorg()
            if len(boards) == 0:
                print 'No ThunderBorg found, check you are attached :)'
            else:
                print 'No ThunderBorg at address %02X, but we did find boards:' % (TB.i2cAddress)
                for board in boards:
                    print '    %02X (%d)' % (board, board)
                print 'If you need to change the I²C address change the setup line so it is correct, e.g.'
                print 'TB.i2cAddress = 0x%02X' % (boards[0])
            sys.exit()

        self.motors = [Motor(self._tb, 0)]

        print '"Robot" loaded!'

    def off(self):
        print 'Unloading Robot'
        self._tb.MotorsOff()
