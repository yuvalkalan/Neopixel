import random
import time
from .neopio import BaseColor


BLACK = BaseColor((0, 0, 0))
WHITE = BaseColor((255, 255, 255))
RED = BaseColor((255, 0, 0))
GREEN = BaseColor((0, 255, 0))
BLUE = BaseColor((0, 0, 255))
YELLOW = BaseColor((255, 255, 0))
MAGENTA = BaseColor((255, 0, 255))
AQUA = BaseColor((0, 255, 255))
COLORS = [RED, GREEN, BLUE, YELLOW, MAGENTA, AQUA]


def led_fade(start, end, delta):
    return int(start + (end - start) * delta)


class Color:
    def __init__(self):
        self._color = BLACK
        self._next_color = random.choice(COLORS)
        self._start_time = None
        self._gen()

    def _gen(self) -> None:
        """
        this function replace the destination color
        :return:
        """
        current = self._color
        self._color = self._next_color
        self._next_color = random.choice([color for color in COLORS if color not in [current, self._color]])
        self._start_time = time.time_ns()

    def get(self, duration, max_bright):
        delta = (time.time_ns() - self._start_time) / 10 ** 9
        if duration <= delta:
            self._gen()
            delta = (time.time_ns() - self._start_time) / 10 ** 9
        brightness = max_bright / 255
        fade_progress = delta / duration
        new_color = BaseColor([led_fade(self._color[i] * brightness,
                                        self._next_color[i] * brightness,
                                        fade_progress) for i in range(3)])
        return new_color.value

