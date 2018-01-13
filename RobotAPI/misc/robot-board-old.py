import smbus
bus = smbus.SMBus(1)

B_I2C_ADR = 0x08

B_PWM_OFFSET = 750
B_PWM_RANGE = 250


# class PWM(object):
#     def __init__(self, command):
#         self._command = command
#
#     @property
#     def value(self):
#         value = bus.read_byte_data(B_I2C_ADR, self._command) + (bus.read_byte_data(B_I2C_ADR, self._command + 1) << 7)
#         return (value - B_PWM_OFFSET) * 100.0 / B_PWM_RANGE
#
#     @value.setter
#     def value(self, percent):
#         value = int((percent / 100.0) * B_PWM_RANGE) + B_PWM_OFFSET
#
#         # high = (value & 0xFF00) >> 8
#         # low = value & 0x00FF
#
#         high = (value & 0b1111111000) >> 3
#         low = value & 0b0000000111
#
#         print
#         print value
#         print "H:", bin(high)
#         print "L:", bin(low)
#
#         bus.write_byte_data(B_I2C_ADR, self._command, low)
#         bus.write_byte_data(B_I2C_ADR, self._command + 1, high)

class PWMList(list):
    # noinspection PyMissingConstructor
    def __init__(self):
        pass

    def __getitem__(self, key):
        command = (2 * key) + 1

        value = bus.read_byte_data(B_I2C_ADR, command) + (bus.read_byte_data(B_I2C_ADR, command + 1) << 7)
        return (value - B_PWM_OFFSET) * 100.0 / B_PWM_RANGE

    def __setitem__(self, key, percent):
        command = (2 * key) + 1

        value = int((percent / 100.0) * B_PWM_RANGE) + B_PWM_OFFSET

        high = (value & 0b1111111000) >> 3
        low = value & 0b0000000111

        bus.write_byte_data(B_I2C_ADR, command, low)
        bus.write_byte_data(B_I2C_ADR, command + 1, high)


class Board(object):
    def __init__(self):
        # self.servos = [
        #     PWM(1),
        #     PWM(3),
        #     PWM(5),
        #     PWM(7)
        # ]
        pass


class Robot(object):
    def __init__(self):
        # self.servos = [
        #     Board()
        # ]

        self.servos = PWMList()


R = Robot()

# R.servos[0].value = 100
# R.servos[0].value = 50
# R.servos[0].value = 0
# R.servos[0].value = -50
# R.servos[0].value = -100

for servo in R.servos:
    print servo

print R.servos[1]



