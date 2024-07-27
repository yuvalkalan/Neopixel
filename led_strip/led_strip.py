import machine
import neopixel
from .settings import Settings
from .color import Color, BLACK
from .constants import *
from .settings.constants import *
from typing import *


class LEDStrip:
    def __init__(self, pin, size, settings: Settings):
        self._np = neopixel.NeoPixel(machine.Pin(pin), size, bpp=3)
        self._size = size
        self._current_poses = []
        self._color = Color()
        self._settings = settings

    def write(self):
        self._np.write()

    def clear(self):
        for i in range(NUM_OF_PIXELS):
            self._np[i] = BLACK

    def start(self):
        for i in range(LINE_LENGTH):
            self._current_poses.append((-i, self._color.get(COLOR_DURATION, self._settings.max_bright)))

    def update(self, data_max: int, data_avg: int, pot_value: int):
        MODE_FUNCTION[self._settings.mode](self, data_max, data_avg, pot_value)

    def update_sound_bar(self, _data_max: int, data_avg: int, _pot_value: int):
        real_value = min(NUM_OF_PIXELS, int(self._settings.sensitivity * NUM_OF_PIXELS * data_avg / 65535))
        for i in range(real_value):
            c = int(i * self._settings.max_bright / NUM_OF_PIXELS)
            self._np[i] = (c, self._settings.max_bright - c, 0)

    def update_sound_route(self, data_max: int, _data_avg: int, _pot_value: int):
        if data_max > self._settings.sensitivity:
            self.start()
        self._current_poses = [(pos + 1, color) for pos, color in self._current_poses if pos + 1 < self._size]
        for pos, color in self._current_poses:
            if pos >= 0:
                self._np[pos] = color

    def update_random_colors(self, _data_max: int, _data_avg: int, _pot_value: int):
        self.update_sound_route(2**32, 0, 0)   # use max value, always triggered

    def update_config_brightness(self, _data_max: int, _data_avg: int, pot_value: int):
        # set all pixel to be at the same color
        v = 255 * pot_value / 65535
        for i in range(NUM_OF_PIXELS):
            self._np[i] = (v, v, v)

    def update_config_sensitivity(self, _data_max: int, _data_avg: int, pot_value: int):
        v = NUM_OF_PIXELS * pot_value / 65535
        for i in range(int(v)):
            c = int(i * self._settings.max_bright / NUM_OF_PIXELS)
            self._np[i] = (c, self._settings.max_bright - c, 0)

    def update_off(self, _data_max: int, _data_avg: int, _pot_value: int):
        pass


MODE_FUNCTION: Dict[int, Callable[int, int, int]] = {MODE_SOUND_BAR: LEDStrip.update_sound_bar,
                                                     MODE_SOUND_ROUTE: LEDStrip.update_sound_route,
                                                     MODE_RANDOM_COLOR: LEDStrip.update_random_colors,
                                                     MODE_CONFIG_BRIGHTNESS: LEDStrip.update_config_brightness,
                                                     MODE_CONFIG_SENSITIVITY: LEDStrip.update_config_sensitivity,
                                                     MODE_OFF: LEDStrip.update_off}
