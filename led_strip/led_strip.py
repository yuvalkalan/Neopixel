import machine
import time
from .settings import Settings
from .color import Color, BLACK, WHITE
from .constants import *


class LEDStrip:
    def __init__(self, pin, size, settings: Settings):
        self._np = neopixel.NeoPixel(machine.Pin(pin), size, bpp=3)
        self._size = size
        self._current_poses = []
        self._color = Color()
        self._settings = settings

    def start(self):
        for i in range(LINE_LENGTH):
            self._current_poses.append((-i, self._color.get()))

    def update(self):
        self._current_poses = [(pos + 1, color) for pos, color in self._current_poses if pos + 1 < self._size]

    def write(self):
        self._np.write()

    def clear(self):
        for i in range(NUM_OF_PIXELS):
            self._np[i] = BLACK

    def update_sound_bar(self, data_value):
        real_value = min(NUM_OF_PIXELS, int(self._settings.volume_sensitivity * NUM_OF_PIXELS * data_value / 65535))
        for i in range(real_value):
            v = int(i * self._settings.max_bright / NUM_OF_PIXELS)
            self._np[i] = (v, self._settings.max_bright - v, 0)

    def update_sound_route(self, data_value):
        if data_value > DATA_THRESHOLD:
            self.start()
        self._current_poses = [(pos + 1, color) for pos, color in self._current_poses if pos + 1 < self._size]
        for pos, color in self._current_poses:
            if pos >= 0:
                self._np[pos] = color
