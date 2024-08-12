from .color import BLACK
import machine
from .constants import *
import rp2
from .dma import DMA


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


class NeoPio:
    def __init__(self, pin):
        self._dma = DMA(NUM_OF_PIXELS)
        self._sm = rp2.StateMachine(0, neopio_asm, freq=20_000_000, set_base=machine.Pin(pin))
        self._sm.active(1)

    def write(self):
        self._dma.start()
        # for v in self._dma:
        #     self._sm.put(v)

    def quit(self):
        self._sm.active(0)

    def __setitem__(self, key, value):
        self._dma[key] = to_bin(value)


def to_bin(color):
    r, g, b = color
    return (g << 16) + (r << 8) + (b << 0)  # color format is grb

