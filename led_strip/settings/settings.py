from .constants import *


class Settings:
    def __init__(self):
        self._mode = MODES[0]
        self._max_bright = DEFAULT_MAX_BRIGHT
        self._sensitivity = DEFAULT_SENSITIVITY

    def update_mode(self):
        new_index = (MODES.index(self._mode) + 1) % len(MODES)
        self._mode = MODES[new_index]
        print(f'new mode is {self._mode}')

    @property
    def mode(self):
        return self._mode

    @property
    def max_bright(self):
        return self._max_bright

    @max_bright.setter
    def max_bright(self, value):
        self._max_bright = value

    @property
    def sensitivity(self):
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        self._sensitivity = value
