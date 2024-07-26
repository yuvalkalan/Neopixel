import machine
import time


class LED:
    def __init__(self, pin):
        self._led = machine.Pin(pin, machine.Pin.OUT)
        self._time = time.time_ns()

    def update(self):
        current_time = time.time_ns()
        if current_time - self._time > 0.5 * 10 ** 9:
            self._led.toggle()
            self._time = current_time
