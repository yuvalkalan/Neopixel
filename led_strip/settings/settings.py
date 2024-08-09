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
        self._config_temp_value = 0

    def update_mode(self):
        new_index = (MODES.index(self._mode) + 1) % len(MODES)
        self._mode = MODES[new_index]
        if self.mode == MODE_CONFIG_SENSITIVITY:
            self._config_temp_value = self._sensitivity
        elif self.mode == MODE_CONFIG_BRIGHTNESS:
            self._config_temp_value = self._max_bright
        elif self.mode == MODE_CONFIG_VOLUME_THRESH:
            self._config_temp_value = self._volume_threshold
        else:
            self._config_temp_value = 0
        print(f'new mode is {self._mode}')

    @property
    def config_temp_value(self):
        return self._config_temp_value

    @config_temp_value.setter
    def config_temp_value(self, value):
        self._config_temp_value = max(0, min(value, 100))

    def reset(self):
        if file_exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        self._max_bright = DEF_MAX_BRIGHT
        self._sensitivity = DEF_SENSITIVITY
        self._volume_threshold = DEF_VOLUME_THRESHOLD
        print('reset settings')

    @property
    def mode(self):
        return self._mode

    @property
    def max_bright_percent(self):
        return self._max_bright

    @max_bright_percent.setter
    def max_bright_percent(self, value):
        self._max_bright = value
        set_settings(self._max_bright, self._sensitivity, self._volume_threshold)

    @property
    def sensitivity_percent(self):
        return self._sensitivity

    @sensitivity_percent.setter
    def sensitivity_percent(self, value):
        self._sensitivity = value
        set_settings(self._max_bright, self._sensitivity, self._volume_threshold)

    @property
    def volume_threshold_percent(self):
        return self._volume_threshold

    @volume_threshold_percent.setter
    def volume_threshold_percent(self, value):
        self._volume_threshold = value
        set_settings(self._max_bright, self._sensitivity, self._volume_threshold)

    @property
    def max_bright(self):
        return int(self._max_bright / 100 * MAX_BRIGHTNESS)

    @property
    def sensitivity(self):
        return int(self._sensitivity / 100 * MAX_SENSITIVITY)

    @property
    def volume_threshold(self):
        return int(self._volume_threshold / 100 * MAX_VOLUME_THRESHOLD)

    @property
    def current_mode_value(self):
        if self._mode == MODE_CONFIG_BRIGHTNESS:
            return self.max_bright
        elif self._mode == MODE_CONFIG_SENSITIVITY:
            return self.sensitivity
        elif self._mode == MODE_CONFIG_VOLUME_THRESH:
            return self.volume_threshold
        return 0
