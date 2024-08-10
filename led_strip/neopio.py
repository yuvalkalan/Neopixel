from .color import BLACK
import machine
from .constants import *
import rp2


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def neopio_asm():
    wrap_target()
    pull()
    out(null, 8)
    label('next_bit')
    out(x, 1)
    jmp(not_x, 'bit_0')
    set(pins, 1)[15]  # 16 cycles = 800ns on
    set(pins, 0)[4]  # 5 + 4 cycles = 450ns off
    jmp('bit_end')

    label('bit_0')
    set(pins, 1)[7]  # 8 cycles = 400ns on
    set(pins, 0)[13]  # 14 + 3 cycles = 850 off
    label('bit_end')
    jmp(not_osre, 'next_bit')
    wrap()


# class Color:
#     def __init__(self, color):
#         self._value = Color.to_bin(color)
#
#     @staticmethod
#     def to_bin(color):
#         r, g, b = color
#         return (g << 16) + (r << 8) + (b << 0)  # color format is grb
#
#     @property
#     def r(self):
#         return (self._value % 2**16) // 2 ** 8
#
#     @r.setter
#     def r(self, r):
#         self._value += (r - self.r) << 8
#
#     @property
#     def g(self):
#         return self._value // 2**16
#
#     @g.setter
#     def g(self, g):
#         self._value += (g - self.g) << 16
#
#     @property
#     def b(self):
#         return self._value % 2**8
#
#     @b.setter
#     def b(self, b):
#         self._value += (b - self.b) << 0
#
#     @property
#     def value(self):
#         return self._value


class NeoPio:
    def __init__(self, pin):
        self._values = [to_bin(BLACK)] * NUM_OF_PIXELS
        self._sm = rp2.StateMachine(0, neopio_asm, freq=20_000_000, set_base=machine.Pin(pin))
        self._sm.active(1)

    def write(self):
        for v in self._values:
            self._sm.put(v)

    def quit(self):
        self._sm.active(0)

    def __setitem__(self, key, value):
        self._values[key] = to_bin(value)


def to_bin(color):
    r, g, b = color
    return (g << 16) + (r << 8) + (b << 0)  # color format is grb

