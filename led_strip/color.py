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
    return int(start + (end - start) * delta)


NS_TIME = 10 ** 9


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
        #         print(brightness)
        #         print(self._color, self._next_color, delta)
        fade_level = delta / duration
        new_color = tuple([led_fade(brightness * self._color[i],
                                    brightness * self._next_color[i],
                                    fade_level) for i in range(3)])
        #         print(new_color)

        #         if new_color == self._next_color:
        #             self._gen()
        # real color after reduce brightness
        #         real_color = tuple([int(v * max_bright / 255) for v in new_color])
        return new_color

