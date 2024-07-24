import machine
import neopixel
import time
import _thread
import random

NUM_OF_PIXELS = 144
NP_PIN = 0
DATA_PIN = 28
POT_PIN = 27
BUTTON_PIN = 15
LED_PIN = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
AQUA = (0, 255, 255)
COLORS = [RED, GREEN, BLUE, YELLOW, MAGENTA, AQUA]

DATA_THRESHOLD = 8000  # 2**15 + 1000
COLOR_DURATION = 3
LINE_LENGTH = 1

DEFAULT_MAX_BRIGHT = 20
DEFAULT_VOLUM_SENSITIVITY = 4

CLOCK_SPEED = 133_000_000

# shared data between threads
running = True
lock = _thread.allocate_lock()

MODE_SOUND_BAR = 1
MODE_SOUND_ROUTE = 2
MODE_RANDOM_COLOR = 3
MODE_OFF = 4

MODES = [MODE_SOUND_BAR,
         MODE_SOUND_ROUTE,
         MODE_RANDOM_COLOR,
         MODE_OFF]

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

        # if button change to down
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


class Settings:
    def __init__(self):
        self._mode = MODES[0]
        self._max_bright = DEFAULT_MAX_BRIGHT
        self._volume_sensitivity = DEFAULT_VOLUM_SENSITIVITY

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
    def volume_sensitivity(self):
        return self._volume_sensitivity

    @volume_sensitivity.setter
    def volume_sensitivity(self, value):
        self._volume_sensitivity = value


class DataRead:
    def __init__(self):
        self._sum = 0
        self._counter = 0
        self._max = 0

    def reset(self):
        self._sum = 0
        self._counter = 0
        self._max = 0

    def __iadd__(self, value):
        self._sum += value
        self._counter += 1
        self._max = max(self._max, value)
        return self

    @property
    def max(self):
        return self._max

    @property
    def avg(self):
        return (self._sum + 0.001) / (self._counter + 0.001)


data_read = DataRead()


def led_fade(start, end, delta):
    return max(0, min(int(start + (end - start) * delta), 255))


class Color:
    def __init__(self):
        self._color = BLACK
        self._next_color = random.choice(COLORS)
        self._start_time = None
        self._gen()

    def _gen(self):
        current = self._color
        self._color = self._next_color
        self._next_color = random.choice([color for color in COLORS if color not in [current, self._color]])
        self._start_time = time.time_ns()

    def get(self):
        delta = (time.time_ns() - self._start_time) / 10 ** 9 / COLOR_DURATION
        new_color = tuple([led_fade(self._color[i], self._next_color[i], delta) for i in range(len(self._color))])
        if new_color == self._next_color:
            self._gen()
        return new_color


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


class LED:
    def __init__(self, pin):
        self._led = machine.Pin(pin, machine.Pin.OUT)
        self._time = time.time_ns()

    def update(self):
        current_time = time.time_ns()
        if current_time - self._time > 0.5 * 10 ** 9:
            self._led.toggle()
            self._time = current_time


def data_thread():
    global data_read
    data_pin = machine.ADC(machine.Pin(DATA_PIN))
    try:
        while running:
            lock.acquire()
            data_read += data_pin.read_u16()
            lock.release()
    finally:
        pass


def main():
    global data_read
    settings = Settings()
    np = LEDStrip(NP_PIN, NUM_OF_PIXELS, settings)
    led = LED(LED_PIN)
    pot = machine.ADC(machine.Pin(POT_PIN))
    button = Button(BUTTON_PIN)
    while True:
        np.clear()
        button.update()
        led.update()
        lock.acquire()
        if button.clicked:
            settings.update_mode()
        data_max, data_avg = data_read.max, data_read.avg
        data_read.reset()
        lock.release()
        if settings.mode == MODE_SOUND_BAR:
            np.update_sound_bar(data_avg)
        elif settings.mode == MODE_SOUND_ROUTE:
            np.update_sound_route(data_max)
        elif settings.mode == MODE_RANDOM_COLOR:
            pass
        np.write()


if __name__ == '__main__':
    machine.freq(CLOCK_SPEED)
    _thread.start_new_thread(data_thread, ())
    try:
        main()
    finally:
        running = False
