import random
import time


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
AQUA = (0, 255, 255)
COLORS = [RED, GREEN, BLUE, YELLOW, MAGENTA, AQUA]


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

    def get(self, duration):
        delta = (time.time_ns() - self._start_time) / 10 ** 9 / duration
        new_color = tuple([led_fade(self._color[i], self._next_color[i], delta) for i in range(len(self._color))])
        if new_color == self._next_color:
            self._gen()
        return new_color
