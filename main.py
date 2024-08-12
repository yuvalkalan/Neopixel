import machine
import _thread
import time
from input import Rotary, AnalogRead
from led import LED
from led_strip import LEDStrip, Settings
from led_strip.settings.constants import *
from led_strip.constants import *

# gpio pins ------------------------------------------------------------------------------------------------------------
NP_PIN = 0
R_DATA_PIN = 28
L_DATA_PIN = 27
CLK_PIN = 18     # yellow
DT_PIN = 17      # green
BUTTON_PIN = 16  # blue
LED_PIN = 25

# system ---------------------------------------------------------------------------------------------------------------
CLOCK_SPEED = 133_000_000
# ----------------------------------------------------------------------------------------------------------------------

# shared data between threads ------------------------------------------------------------------------------------------
running = True
lock = _thread.allocate_lock()
rotary = Rotary(CLK_PIN, DT_PIN, BUTTON_PIN)
r_data = AnalogRead()
l_data = AnalogRead()
data_thread_running = False
# ----------------------------------------------------------------------------------------------------------------------


def data_thread():
    global r_data
    global l_data
    global data_thread_running

    with lock:
        data_thread_running = True
    r_data_pin = machine.ADC(machine.Pin(R_DATA_PIN))
    l_data_pin = machine.ADC(machine.Pin(L_DATA_PIN))
    while running:
        with lock:
            r_data += r_data_pin.read_u16()
            l_data += l_data_pin.read_u16()
            rotary.update()
    data_thread_running = False
    print('closing second tread...')


def main():
    global r_data
    global l_data

    settings = Settings()
    np = LEDStrip(NP_PIN, NUM_OF_PIXELS, settings)
    led = LED(LED_PIN)
    counter = 0
    a = time.time_ns()
    while True:
        np.clear()
        led.update()
        rotary.update_button()
        spin = rotary.spin
        settings.config_temp_value += spin
        with lock:
            r_data_max, r_data_avg = r_data.max, r_data.avg
            r_data.reset()
            l_data_max, l_data_avg = l_data.max, l_data.avg
            l_data.reset()
            if rotary.clicked:
                settings.update_mode()
                np.reset()
            elif rotary.double_clicked:
                if settings.mode == MODE_CONFIG_SENSITIVITY:
                    settings.sensitivity_percent = settings.config_temp_value
                    settings.update_mode()
                elif settings.mode == MODE_CONFIG_BRIGHTNESS:
                    settings.max_bright_percent = settings.config_temp_value
                    settings.update_mode()
                elif settings.mode == MODE_CONFIG_VOLUME_THRESH:
                    settings.volume_threshold_percent = settings.config_temp_value
                    settings.update_mode()
            elif rotary.hold_down:
                settings.reset()
        np.update(r_data_max, r_data_avg, l_data_max, l_data_avg, settings.config_temp_value)
        np.write()
        counter += 1
        if counter % 50 == 0:
            b = time.time_ns()
            print(50/((b-a)/10**9))
            a = b
            counter = 0


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
        time.sleep(0.5)
    print('finish')
