import RPi.GPIO as GPIO
from firebase_admin import db


LED_PINS = [5, 13, 21]
_last_state = None

def setup():
    global _last_state
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in LED_PINS:
        GPIO.setup(pin, GPIO.OUT)
    _last_state = None  

def update_led():
    global _last_state
    led_ref = db.reference('led')
    state = led_ref.get()

    is_on = str(state).strip().lower() == 'true'

    if is_on != _last_state:
        _last_state = is_on
        for pin in LED_PINS:
            GPIO.output(pin, GPIO.HIGH if is_on else GPIO.LOW)
        print("LED ON" if is_on else "LED OFF")
            
def set_led(state: bool):
    global _last_state
    if state != _last_state:
        _last_state = state
        for pin in LED_PINS:
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
        print("LED ON" if state else "LED OFF")

def cleanup():
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()
