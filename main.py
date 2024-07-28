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
    print('closing second tread...')


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
            data_max, data_avg = data.max, data.avg
            data.reset()
            pot_value = pot.read_u16()
            if button.clicked:
                settings.update_mode()
                np.reset()
            elif button.double_clicked:
                if settings.mode == MODE_CONFIG_SENSITIVITY:
                    settings.sensitivity = MAX_SENSITIVITY * pot_value / 65535
                    settings.update_mode()
                elif settings.mode == MODE_CONFIG_BRIGHTNESS:
                    settings.max_bright = int(MAX_BRIGHTNESS * pot_value / 65535)
                    settings.update_mode()
            elif button.hold_down:
                settings.reset()

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
        print('waiting for second thread...')
        time.sleep(0.1)
    print('finish')
