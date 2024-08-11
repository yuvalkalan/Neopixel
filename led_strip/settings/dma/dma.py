import array
from machine import mem8, mem16, mem32
from .constants import *


class DMA:
    def __init__(self, length):
        self._buffer = array.array('L', [0]*length)
        self._length = length
        self._disable()

    @property
    def _array_id(self):
        return mem32[id(self._buffer) + 12]

    def config(self):
        mem32[CH0_READ_ADDR] = self._array_id   # Source address (start of data array)
        mem32[CH0_WRITE_ADDR] = PIO0_TXF0       # Destination address (PIO TX FIFO)
        mem32[CH0_TRANS_COUNT] = self._length   # Number of words to transfer

    @property
    def busy(self):
        return (mem32[CH0_CTRL_TRIG] >> 24) % 2 == 1

    @staticmethod
    def _enable():
        # set ctrl_en to 1
        mem32[CH0_CTRL_TRIG] = CTRL_CONFIG + 1 * 2 ** CTRL_EN

    @staticmethod
    def _disable():
        # set ctrl_en to 0
        mem32[CH0_CTRL_TRIG] = CTRL_CONFIG + 0 * 2 ** CTRL_EN

    def __setitem__(self, key, value):
        self._buffer[key] = value

    def start(self):
        while self.busy:    # wait until free
            pass
        self._disable()     # stop
        self.config()       # config
        self._enable()      # start
