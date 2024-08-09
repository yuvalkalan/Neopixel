import time

import machine
import neopixel
from .settings import Settings
from .color import Color, BLACK
from .constants import *
from .settings.constants import *


class LED:
    def __init__(self, color, rtl: bool):
        """

        :param color:
        :param rtl: true -> rtl, false -> lrt
        """
        self._color = color
        self._rtl = rtl
        self._index = 0

    def update(self):
        self._index += 1
        return self.alive

    @property
    def color(self):
        return self._color

    @property
    def index(self):
        return self._index if self._rtl else NUM_OF_PIXELS - self._index - 1

    @property
    def alive(self):
        return self._index <= NUM_OF_PIXELS / 2


class LEDStrip:
    def __init__(self, pin, size, settings: Settings):
        self._np = neopixel.NeoPixel(machine.Pin(pin), size, bpp=3)
        self._size = size
        self._current_leds = []
        self._color = Color()
        self._settings = settings
        self._time = time.time_ns()
        self._counter = 1

    def write(self):
        self._np.write()

    def clear(self):
        for i in range(NUM_OF_PIXELS):
            self._np[i] = BLACK

    def _start(self, rtl):
        color = self._color.get(COLOR_DURATION, self._settings.max_bright)
        self._current_leds.append(LED(color, rtl))

    def _draw(self):
        for led in self._current_leds:
            self._np[led.index] = led.color
        self._current_leds = [led for led in self._current_leds if led.update()]

    def update(self, r_data_max: int, r_data_avg: int, l_data_max: int, l_data_avg: int, rotary_value: int):
        MODE_FUNCTION[self._settings.mode](self, r_data_max, r_data_avg, l_data_max, l_data_avg, rotary_value)

    def update_sound_bar(self, _r_data_max: int, r_data_avg: int, _l_data_max: int, _l_data_avg: int, _rotary_value: int):
        real_value = min(NUM_OF_PIXELS, int(self._settings.sensitivity * NUM_OF_PIXELS * r_data_avg / 65535))
        for i in range(real_value):
            c = int(i * self._settings.max_bright / NUM_OF_PIXELS)
            self._np[i] = (c, self._settings.max_bright - c, 0)

    def update_sound_route(self, r_data_max: int, _r_data_avg: int, l_data_max: int, _l_data_avg: int, _rotary_value: int):
        if r_data_max > self._settings.volume_threshold:
            self._start(True)
        if l_data_max > self._settings.volume_threshold:
            self._start(False)
        self._draw()

    def update_random_colors(self, _r_data_max: int, _r_data_avg: int, _l_data_max: int, _l_data_avg: int, _rotary_value: int):
        self.update_sound_route(2 ** 32, 0, 2**32, 0, 0)  # use max value, always triggered

    def update_config_brightness(self, _r_data_max: int, _r_data_avg: int, _l_data_max: int, _l_data_avg: int,
                                 rotary_value: int):
        # set all pixels to be at the same color
        v = int(255 * rotary_value / 100)
        print(rotary_value, v)

        for i in range(NUM_OF_PIXELS):
            self._np[i] = (v, v, v)

    def update_config_sensitivity(self, _r_data_max: int, _r_data_avg: int, _l_data_max: int, _l_data_avg: int,
                                  rotary_value: int):
        v = NUM_OF_PIXELS * rotary_value / 100
        for i in range(int(v)):
            c = int(i * self._settings.max_bright / NUM_OF_PIXELS)
            self._np[i] = (c, self._settings.max_bright - c, 0)

    def update_config_volume_thresh(self, _r_data_max: int, _r_data_avg: int, _l_data_max: int, _l_data_avg: int,
                                    rotary_value: int):
        freq = max(int(NUM_OF_PIXELS * (rotary_value / 100)), 1)  # counter / pixel
        print(rotary_value, freq, self._counter, self._counter // freq)
        if self._counter // freq != 0:
            self._start(True)
            self._start(False)
            self._counter -= freq
        self._counter += 1
        self._draw()

    def update_off(self, _r_data_max: int, _r_data_avg: int, _l_data_max: int, _l_data_avg: int, _rotary_value: int):
        pass

    def reset(self):
        self._current_leds = []


MODE_FUNCTION = {MODE_SOUND_BAR: LEDStrip.update_sound_bar,
                 MODE_SOUND_ROUTE: LEDStrip.update_sound_route,
                 MODE_RANDOM_COLOR: LEDStrip.update_random_colors,
                 MODE_CONFIG_BRIGHTNESS: LEDStrip.update_config_brightness,
                 MODE_CONFIG_SENSITIVITY: LEDStrip.update_config_sensitivity,
                 MODE_CONFIG_VOLUME_THRESH: LEDStrip.update_config_volume_thresh,
                 MODE_OFF: LEDStrip.update_off}


