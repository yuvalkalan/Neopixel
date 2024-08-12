import time


class Clock:
    def __init__(self, refresh_rate):
        self._refresh_rate = refresh_rate
        self._frequency = 1.0 / refresh_rate
        self._last_frame_time = time.time_ns()
        self._delta = 0

    def tick(self):
        current_time = time.time_ns()
        while (current_time - self._last_frame_time) / 10**9 + self._delta < self._frequency:
            current_time = time.time_ns()
        self._delta += (current_time - self._last_frame_time) / 10**9 - self._frequency
        self._last_frame_time = current_time
        return self._delta

