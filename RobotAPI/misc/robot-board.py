import smbus
bus = smbus.SMBus(1)

B_I2C_ADR = 0x08

B_I2C_GPIO_ANALOGUE_START_L = 11
# B_I2C_GPIO_ANALOGUE_1_L = 11
# B_I2C_GPIO_ANALOGUE_1_H = 12
# B_I2C_GPIO_ANALOGUE_3_L = 13
# B_I2C_GPIO_ANALOGUE_3_H = 14
# B_I2C_GPIO_ANALOGUE_4_L = 15
# B_I2C_GPIO_ANALOGUE_4_H = 16

B_I2C_GPIO_CONTROL_START = 17
# B_I2C_GPIO_CONTROL_1 = 17
# B_I2C_GPIO_CONTROL_2 = 18
# B_I2C_GPIO_CONTROL_3 = 19
# B_I2C_GPIO_CONTROL_4 = 20

B_I2C_GPIO_START = 21
# B_I2C_GPIO_1 = 21
# B_I2C_GPIO_2 = 22
# B_I2C_GPIO_3 = 23
# B_I2C_GPIO_4 = 24

B_PWM_OFFSET = 750
B_PWM_RANGE = 250


class BoardPWM(object):
    def __getitem__(self, key):
        if key < 0 or key > 3:
            raise IndexError("PWM index must be between 0 and 3")
        command = (2 * key) + 1

        print command

        value = bus.read_byte_data(B_I2C_ADR, command) + (bus.read_byte_data(B_I2C_ADR, command + 1) << 7)
        return (value - B_PWM_OFFSET) * 100.0 / B_PWM_RANGE

    def __setitem__(self, key, percent):
        if key < 0 or key > 3:
            raise IndexError("PWM index must be between 0 and 3")
        command = (2 * key) + 1

        value = int((percent / 100.0) * B_PWM_RANGE) + B_PWM_OFFSET

        high = (value & 0b1111111000) >> 3
        low = value & 0b0000000111

        print
        print value
        print "H:", bin(high)
        print "L:", bin(low)

        bus.write_byte_data(B_I2C_ADR, command, low)
        bus.write_byte_data(B_I2C_ADR, command + 1, high)


INPUT = 0
OUTPUT = 1
INPUT_ANALOGUE = 2
INPUT_PULLUP = 3


# noinspection PyMethodMayBeStatic
class BoardGPIO(object):
    def pin_mode(self, pin, mode):
        data = 0b000

        if mode == INPUT or mode == OUTPUT:
            data = 0b001
        if mode == INPUT_PULLUP:
            data = 0b101
        if mode == INPUT_ANALOGUE:
            data = 0b010

        bus.write_byte_data(B_I2C_ADR, B_I2C_GPIO_CONTROL_START + pin - 1, data)

    def digital_read(self, pin):
        return bool(bus.read_byte_data(B_I2C_ADR, B_I2C_GPIO_START + pin - 1))

    def analog_read(self, pin):
        command = B_I2C_GPIO_ANALOGUE_START_L + (2 * (pin - 1))
        return bus.read_byte_data(B_I2C_ADR, command) + (bus.read_byte_data(B_I2C_ADR, command + 1) << 7)

    def digital_write(self, pin, data):
        bus.write_byte_data(B_I2C_ADR, B_I2C_GPIO_START + pin - 1, int(data))


class Robot(object):
    def __init__(self):
        self.servos = BoardPWM()
        self.gpio = BoardGPIO()


R = Robot()

# R.servos[-1] = 90
# print R.servos[5]

# R.servos[0] = 100
# R.servos[0] = 50
# R.servos[0] = 0
# R.servos[0] = -50
# R.servos[0] = -100

R.gpio.pin_mode(1, INPUT)


