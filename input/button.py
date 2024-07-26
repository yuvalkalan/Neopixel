import machine
import time


MAX_DOUBLE_CLICK_DELTA = 0.5
HOLD_DOWN_THRESHOLD = 0.3


class Button:
    def __init__(self, pin):
        self._button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)  # gpio
        self._value = self._button.value()  # raw value
        self._last_click_time = None  # last click timer
        self._press_time = None  # hold down timer
        self._has_changed = False
        self._has_click = False
        self._has_double_click = False
        self._has_hold_down = False
        self._got_hold_down = False  # hold lock

    def _reset(self):
        self._has_changed = False
        self._has_click = False
        self._has_double_click = False
        self._has_hold_down = False

    def update(self):
        self._reset()
        # read current value
        value = self._button.value()
        # set has_changed value
        self._has_changed = value != self._value
        # get current time
        t = time.time_ns()

        # if clicked, check if timeout for double click
        if self._last_click_time and (t - self._last_click_time) / 10 ** 9 > MAX_DOUBLE_CLICK_DELTA:
            self._last_click_time = None
            self._has_click = True

        # if input change to down
        if value == 0:
            if self._has_changed:
                # if already got clicked once, set double click
                if self._last_click_time:
                    self._has_double_click = True
                    self._last_click_time = None
                else:
                    self._last_click_time = t
                # set hold timer to current time
                self._press_time = t
        else:
            # reset press time if value is up
            self._press_time = None

        # if hold press
        if self._press_time and (t - self._press_time) / 10 ** 9 > HOLD_DOWN_THRESHOLD:
            self._has_hold_down = True and not self._got_hold_down
            self._got_hold_down = True
            self._last_click_time = None
        else:
            self._got_hold_down = False
        self._value = value

    @property
    def is_changed(self):
        return self._has_changed

    @property
    def is_down(self):
        return self._value == 0

    @property
    def is_up(self):
        return not self.is_down

    @property
    def clicked(self):
        return self._has_click

    @property
    def double_clicked(self):
        return self._has_double_click

    @property
    def hold_down(self):
        return self._has_hold_down