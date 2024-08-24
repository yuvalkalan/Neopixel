from .button import Button
import machine


class Rotary:
    def __init__(self, pin_clk, pin_dt, pin_y):
        self._clk = machine.Pin(pin_clk)
        self._dt = machine.Pin(pin_dt)
        self._clk_last_value = self._clk.value()
        self._spin = 0
        self._btn = Button(pin_y)

    def update_button(self):
        self._btn.update()

    def update(self):
        clk_state = self._clk.value()
        dt_state = self._dt.value()
        if clk_state != self._clk_last_value and self._clk_last_value:
            if dt_state != clk_state:
                self._spin += 1
            else:
                self._spin -= 1
        self._clk_last_value = clk_state

    @property
    def spin(self):
        v = self._spin
        self._spin = 0
        return v

    @property
    def is_down(self):
        return self._btn.is_down

    @property
    def is_up(self):
        return self._btn.is_up

    @property
    def clicked(self):
        return self._btn.clicked

    @property
    def double_clicked(self):
        return self._btn.double_clicked

    @property
    def hold_down(self):
        return self._btn.hold_down
