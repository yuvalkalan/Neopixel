import machine
import _thread
import time
from input import Button, AnalogRead
from led import LED
from led_strip import LEDStrip, Settings
from led_strip.settings.constants import *
from led_strip.constants import *

# gpio pins ------------------------------------------------------------------------------------------------------------
NP_PIN = 0
DATA_PIN = 28
POT_PIN = 27
BUTTON_PIN = 15
LED_PIN = 25
# ----------------------------------------------------------------------------------------------------------------------

DATA_THRESHOLD = 8000  # 2**15 + 1000

# system ---------------------------------------------------------------------------------------------------------------
CLOCK_SPEED = 133_000_000
# ----------------------------------------------------------------------------------------------------------------------

# shared data between threads ------------------------------------------------------------------------------------------
running = True
lock = _thread.allocate_lock()
data = AnalogRead()
data_thread_running = False
# ----------------------------------------------------------------------------------------------------------------------


def data_thread():
    global data
    global data_thread_running

    with lock:
        data_thread_running = True
    data_pin = machine.ADC(machine.Pin(DATA_PIN))
    while running:
        with lock:
            data += data_pin.read_u16()
    data_thread_running = False


def main():
    global data

    settings = Settings()
    np = LEDStrip(NP_PIN, NUM_OF_PIXELS, settings)
    led = LED(LED_PIN)
    pot = machine.ADC(machine.Pin(POT_PIN))
    button = Button(BUTTON_PIN)
    while True:
        np.clear()
        button.update()
        led.update()
        with lock:
            if button.clicked:
                settings.update_mode()
            data_max, data_avg = data.max, data.avg
            pot_value = pot.read_u16()
            data.reset()
        np.update(data_max, data_avg, pot_value)
        np.write()


if __name__ == '__main__':
    machine.freq(CLOCK_SPEED)
    _thread.start_new_thread(data_thread, ())
    try:
        main()
    finally:
        with lock:
            running = False
    while data_thread_running:  # wait until second thread close
        time.sleep(0.1)

