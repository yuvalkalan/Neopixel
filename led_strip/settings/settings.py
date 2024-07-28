from .constants import *
import ujson
import os


def file_exists(filename) -> bool:
    try:
        os.stat(filename)
        return True
    except OSError:
        return False


def set_settings(max_bright: int, sensitivity: float, volume_threshold) -> None:
    with open(SETTINGS_FILE, 'w') as json_file:
        json_file.write(ujson.dumps({SETTING_MAX_BRIGHT: max_bright,
                                     SETTING_SENSITIVITY: sensitivity,
                                     SETTING_VOLUME_THRESHOLD: volume_threshold}))


def get_settings():
    with open(SETTINGS_FILE, 'r') as json_file:
        data = ujson.loads(json_file.read())
    return data[SETTING_MAX_BRIGHT], data[SETTING_SENSITIVITY], data[SETTING_VOLUME_THRESHOLD]


class Settings:
    def __init__(self):
        self._mode = MODES[0]
        if file_exists(SETTINGS_FILE):
            max_bright, sensitivity, volume_threshold = get_settings()
        else:
            max_bright, sensitivity, volume_threshold = DEF_MAX_BRIGHT, DEF_SENSITIVITY, DEF_VOLUME_THRESHOLD

        self._max_bright = max_bright
        self._sensitivity = sensitivity
        self._volume_threshold = volume_threshold

    def update_mode(self):
        new_index = (MODES.index(self._mode) + 1) % len(MODES)
        self._mode = MODES[new_index]
        print(f'new mode is {self._mode}')

    def reset(self):
        if file_exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        self._max_bright = DEF_MAX_BRIGHT
        self._sensitivity = DEF_SENSITIVITY
        self._volume_threshold = DEF_VOLUME_THRESHOLD

    @property
    def mode(self):
        return self._mode

    @property
    def max_bright(self):
        return self._max_bright

    @max_bright.setter
    def max_bright(self, value):
        self._max_bright = value
        set_settings(self._max_bright, self._sensitivity, self._volume_threshold)

    @property
    def sensitivity(self):
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        self._sensitivity = value
        set_settings(self._max_bright, self._sensitivity, self._volume_threshold)

    @property
    def volume_threshold(self):
        return self._volume_threshold


    @volume_threshold.setter
    def volume_threshold(self, value):
        self._volume_threshold = value
        set_settings(self._max_bright, self._sensitivity, self._volume_threshold)

