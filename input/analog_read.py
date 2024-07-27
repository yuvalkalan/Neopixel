class AnalogRead:
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
        return (self._sum + 0.001) // (self._counter + 0.001)
