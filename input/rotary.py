from .button import Button
import machine


class Rotary:
    def __init__(self, pin_clk, pin_dt, pin_y):
        self._clk = machine.Pin(pin_clk)
        self._dt = machine.Pin(pin_dt)
        self._clk_last_value = self._clk.value()
        self._spin = 0
        self._y = Button(pin_y)

    def update_button(self):
        self._y.update()

    def update(self):
        clk_state = self._clk.value()
        dt_state = self._dt.value()
        if clk_state != self._clk_last_value and self._clk_last_value:
            if dt_state != clk_state:
                self._spin = 1
            else:
                self._spin = -1
        else:
            self._spin = 0
        self._clk_last_value = clk_state

    @property
    def spin(self):
        return self._spin

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
