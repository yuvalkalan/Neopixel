from .button import Button


class Rotary:
    def __init__(self, pin_clk, pin_dt, pin_y):
        self._clk = machine.Pin(pin_clk)
        self._dt = machine.Pin(pin_dt)
        self._clk_last_value = self._clk.value()
        self._direction = 0
        self._y = Button(pin_y)

    def update(self):
        self._y.update()
        clk_state = self._clk.value()
        dt_state = self._dt.value()
        if clk_state != self._clk_last_value and self._clk_last_value:
            if dt_state != clk_state:
                self._direction = 1
            else:
                self._direction = -1
        else:
            self._direction = 0
        self._clk_last_value = clk_state

    @property
    def direction(self):
        return self._direction

    @property
    def is_down(self):
        return self._y.is_down

    @property
    def is_up(self):
        return self._y.is_up

    @property
    def clicked(self):
        return self._y.clicked

    @property
    def double_clicked(self):
        return self._y.double_clicked

    @property
    def hold_down(self):
        return self._y.hold_down
