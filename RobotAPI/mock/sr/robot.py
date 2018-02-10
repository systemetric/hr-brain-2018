#!/usr/bin/env python
# coding: latin-1

B_PWM_OFFSET = 256
B_PWM_RANGE = 256

INPUT = 0
OUTPUT = 1
INPUT_ANALOG = 2
INPUT_PULLUP = 3

GPIO_PIN_MAP = {
    4: 1,
    3: 2,
    2: 4,
    1: 3
}

SERVO_PIN_MAP = {
    1: 3,
    2: 1,
    3: 2,
    4: 4
}


class MockThunderBorgMotorChannel(object):
    def __init__(self, index):
        self._index = index

        self._motor_1 = 0
        self._motor_2 = 0

    @property
    def power(self):
        if self._index == 0:
            print "ROBOT: Getting 1st motor's power at", self._motor_1 * 100.0
            return self._motor_1 * 100.0
        else:
            print "ROBOT: Getting 2nd motor's power at", self._motor_2 * 100.0
            return self._motor_2 * 100.0

    @power.setter
    def power(self, value):
        if self._index == 0:
            self._motor_1 = (float(value) / 100.0)
            print "ROBOT: Setting 1st motor's power to", value
        else:
            self._motor_2 = (float(value) / 100.0)
            print "ROBOT: Setting 2nd motor's power to", value


class MockThunderBorgLED(object):
    def __init__(self):
        self._led = (0, 0, 0)
        pass

    @property
    def colour(self):
        print "ROBOT: Getting LED colour at", self._led
        return self._led

    @colour.setter
    def colour(self, value):
        self._led = (float(value[0]) / 255.0, float(value[1]) / 255.0, float(value[2]) / 255.0)
        print "ROBOT: Setting LED colour to", self._led

    def off(self):
        print "ROBOT: Turning LED off", self._led
        pass


class MockThunderBorgBoard(object):
    def __init__(self):
        self.m0 = MockThunderBorgMotorChannel(0)
        self.m1 = MockThunderBorgMotorChannel(1)
        self.led = MockThunderBorgLED()

    # noinspection PyMethodMayBeStatic
    def off(self):
        print "ROBOT: Turning motor board off"
        pass


class MockBlackJackBoardPWM(object):
    def __init__(self):
        self._data = [0, 0, 0, 0, 0, 0, 0, 0]

    def __getitem__(self, key):
        if key < 0 or key > 3:
            raise IndexError("PWM index must be between 0 and 3")
        key = SERVO_PIN_MAP[key + 1] - 1
        command = (2 * key) + 1

        value = self._data[command] + (self._data[command + 1] << 7)
        percent = (value - B_PWM_OFFSET) * 100.0 / B_PWM_RANGE
        print "ROBOT: Getting servo", key + 1, "at", percent, "% [ PWM:", value, "]"
        return percent

    def __setitem__(self, key, percent):
        if key < 0 or key > 3:
            raise IndexError("PWM index must be between 0 and 3")
        key = SERVO_PIN_MAP[key + 1] - 1
        command = (2 * key) + 1

        value = int((percent / 100.0) * B_PWM_RANGE) + B_PWM_OFFSET

        high = value >> 7
        low = value & 0x7F

        print "ROBOT: Setting servo", key + 1, "to", percent, "% [ PWM:", value, "]"

        self._data[command] = low
        self._data[command + 1] = high


class MockBlackJackBoardGPIO(object):
    def __init__(self):
        self._data = [0, 0, 0, 0]

    def pin_mode(self, pin, mode):
        pin = GPIO_PIN_MAP[pin]
        if pin == 2 and mode == INPUT_ANALOG:
            raise IndexError("Pin 3 is NOT an ANALOG input! Use something else!")

        data = 0b000

        if mode == INPUT:
            print "ROBOT: Setting mode of pin", pin, "to INPUT"
            data = 0b001
        elif mode == INPUT_PULLUP:
            print "ROBOT: Setting mode of pin", pin, "to INPUT_PULLUP"
            data = 0b101
        elif mode == INPUT_ANALOG:
            print "ROBOT: Setting mode of pin", pin, "to INPUT_ANALOG"
            data = 0b011
        else:
            print "ROBOT: Setting mode of pin", pin, "to OUTPUT"

        self._data[pin - 1] = data

    def digital_read(self, pin):
        pin = GPIO_PIN_MAP[pin]
        v = bool(self._data[pin - 1])
        print "ROBOT: Getting pin", pin, "digital value at", v
        return v

    # noinspection PyMethodMayBeStatic
    def analog_read(self, pin):
        pin = GPIO_PIN_MAP[pin]
        if pin == 2:
            raise IndexError("Pin 3 is NOT an ANALOG input! Use something else!")
        print "ROBOT: Getting pin", pin, "analog value at 0 (MOCK ROBOT DOESN'T DO ANALOG INPUT)"
        return 0

    def digital_write(self, pin, data):
        pin = GPIO_PIN_MAP[pin]
        print "ROBOT: Setting pin", pin, "digital value to", data
        self._data[pin - 1] = int(data)


class Robot(object):
    def __init__(self):
        self.motors = [
            MockThunderBorgBoard(),
            MockThunderBorgBoard(),
            MockThunderBorgBoard(),
            MockThunderBorgBoard()
        ]

        self.servos = MockBlackJackBoardPWM()
        self.gpio = MockBlackJackBoardGPIO()
        print "ROBOT: Initialised"

    def off(self):
        print "ROBOT: Switching off"
        for motor in self.motors:
            motor.off()

    # noinspection PyMethodMayBeStatic
    def see(self, res, save):
        print "ROBOT: Seeing things (MOCK ROBOT ALWAYS RETURNS EMPTY MARKET SET)"
        return []
