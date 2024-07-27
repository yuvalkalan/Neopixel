from .constants import *
import ujson
import os
from typing import *


# settings -------------------------------------------------------------------------------------------------------------
SETTINGS_FILE = 'settings.json'
SETTING_MAX_BRIGHT = 'max_bright'
SETTING_SENSITIVITY = 'sensitivity'
# ----------------------------------------------------------------------------------------------------------------------


def file_exists(filename) -> bool:
    try:
        os.stat(filename)
        return True
    except OSError:
        return False


def set_settings(max_bright: int, sensitivity: float) -> None:
    with open(SETTINGS_FILE, 'w') as json_file:
        json_file.write(ujson.dumps({SETTING_MAX_BRIGHT: max_bright,
                                     SETTING_SENSITIVITY: sensitivity}))


def get_settings() -> Tuple[int, float]:
    with open(SETTINGS_FILE, 'r') as json_file:
        data = ujson.loads(json_file.read())
    return data[SETTING_MAX_BRIGHT], data[SETTING_SENSITIVITY]


class Settings:
    def __init__(self):
        self._mode = MODES[0]
        if file_exists(SETTINGS_FILE):
            max_bright, sensitivity = get_settings()
        else:
            max_bright, sensitivity = DEFAULT_MAX_BRIGHT, DEFAULT_SENSITIVITY

        self._max_bright = max_bright
        self._sensitivity = sensitivity

    def update_mode(self):
        new_index = (MODES.index(self._mode) + 1) % len(MODES)
        self._mode = MODES[new_index]
        print(f'new mode is {self._mode}')

    def reset(self):
        if file_exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        self._max_bright = DEFAULT_MAX_BRIGHT
        self._sensitivity = DEFAULT_SENSITIVITY

    @property
    def mode(self):
        return self._mode

    @property
    def max_bright(self):
        return self._max_bright

    @max_bright.setter
    def max_bright(self, value):
        self._max_bright = value
        set_settings(self._max_bright, self._sensitivity)

    @property
    def sensitivity(self):
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        self._sensitivity = value
        set_settings(self._max_bright, self._sensitivity)
