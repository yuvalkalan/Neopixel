# modes ----------------------------------------------------------------------------------------------------------------
MODE_SOUND_BAR = 1
MODE_SOUND_ROUTE = 2
MODE_RANDOM_COLOR = 3
MODE_CONFIG_BRIGHTNESS = 4
MODE_CONFIG_SENSITIVITY = 5
MODE_CONFIG_VOLUME_THRESH = 6
MODE_OFF = 7
MODES = [MODE_SOUND_BAR,
         MODE_SOUND_ROUTE,
         MODE_RANDOM_COLOR,
         MODE_CONFIG_BRIGHTNESS,
         MODE_CONFIG_SENSITIVITY,
         MODE_CONFIG_VOLUME_THRESH,
         MODE_OFF]
# ----------------------------------------------------------------------------------------------------------------------

# default values -------------------------------------------------------------------------------------------------------
MAX_SENSITIVITY = 20
MAX_BRIGHTNESS = 255
MAX_VOLUME_THRESHOLD = 65535

DEF_MAX_BRIGHT = 10             # 10%
DEF_SENSITIVITY = 25            # 25%
DEF_VOLUME_THRESHOLD = 9        # 9%
# ----------------------------------------------------------------------------------------------------------------------

# settings json file ---------------------------------------------------------------------------------------------------
SETTINGS_FILE = 'settings.json'
SETTING_MAX_BRIGHT = 'max_bright'
SETTING_SENSITIVITY = 'sensitivity'
SETTING_VOLUME_THRESHOLD = 'volume_threshold'
# ----------------------------------------------------------------------------------------------------------------------
