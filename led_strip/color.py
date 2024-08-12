import random
import time
from .neopio import BaseColor


NS_TIME = 10 ** 9


def led_fade(start, end, delta):
    return max(0, min(int(start + (end - start) * delta), 255))


BLACK = BaseColor((0, 0, 0))
WHITE = BaseColor((255, 255, 255))
RED = BaseColor((255, 0, 0))
GREEN = BaseColor((0, 255, 0))
BLUE = BaseColor((0, 0, 255))
YELLOW = BaseColor((255, 255, 0))
MAGENTA = BaseColor((255, 0, 255))
AQUA = BaseColor((0, 255, 255))
COLORS = [RED, GREEN, BLUE, YELLOW, MAGENTA, AQUA]


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
        delta = (time.time_ns() - self._start_time) / NS_TIME
        if duration <= delta:
            self._gen()
            delta = (time.time_ns() - self._start_time) / NS_TIME
        brightness = max_bright / 255
        fade_level = delta / duration
        new_color = BaseColor([led_fade(brightness*self._color[i],
                                        brightness*self._next_color[i],
                                        fade_level) for i in range(3)])
        return new_color
