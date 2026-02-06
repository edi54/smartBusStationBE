import RPi.GPIO as GPIO

# RGB LED 1
RED_PIN_1 = 4
BLUE_PIN_1 = 27
GREEN_PIN_1 = 17

# RGB LED 2
RED_PIN_2 = 24
BLUE_PIN_2 = 22
GREEN_PIN_2 = 25

_last_value_1 = None
_last_value_2 = None

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_PIN_1, GPIO.OUT)
    GPIO.setup(BLUE_PIN_1, GPIO.OUT)
    GPIO.setup(GREEN_PIN_1, GPIO.OUT)
    GPIO.setup(RED_PIN_2, GPIO.OUT)
    GPIO.setup(BLUE_PIN_2, GPIO.OUT)
    GPIO.setup(GREEN_PIN_2, GPIO.OUT)

    GPIO.output(RED_PIN_1, GPIO.LOW)
    GPIO.output(BLUE_PIN_1, GPIO.LOW)
    GPIO.output(GREEN_PIN_1, GPIO.LOW)
    GPIO.output(RED_PIN_2, GPIO.LOW)
    GPIO.output(BLUE_PIN_2, GPIO.LOW)
    GPIO.output(GREEN_PIN_2, GPIO.LOW)

def update_led_1(value):
    global _last_value_1
    if value == _last_value_1:
        return
    _last_value_1 = value
    print(f"[RGB1] chair_1: {value}")

    if value == 0:
        GPIO.output(RED_PIN_1, GPIO.LOW)
        GPIO.output(BLUE_PIN_1, GPIO.LOW)
        GPIO.output(GREEN_PIN_1, GPIO.LOW)
        print("[RGB1] GREEN")
    elif value == 1:
        GPIO.output(RED_PIN_1, GPIO.LOW)
        GPIO.output(BLUE_PIN_1, GPIO.HIGH)
        GPIO.output(GREEN_PIN_1, GPIO.LOW)
        print("[RGB1] BLUE")
    elif value == 2:
        GPIO.output(RED_PIN_1, GPIO.HIGH)
        GPIO.output(BLUE_PIN_1, GPIO.LOW)
        GPIO.output(GREEN_PIN_1, GPIO.LOW)
        print("[RGB1] RED")

def update_led_2(value):
    global _last_value_2
    if value == _last_value_2:
        return
    _last_value_2 = value
    print(f"[RGB2] chair_2: {value}")

    if value == 0:
        GPIO.output(RED_PIN_2, GPIO.LOW)
        GPIO.output(BLUE_PIN_2, GPIO.LOW)
        GPIO.output(GREEN_PIN_2, GPIO.LOW)
        print("[RGB2] GREEN")
    elif value == 1:
        GPIO.output(RED_PIN_2, GPIO.LOW)
        GPIO.output(BLUE_PIN_2, GPIO.HIGH)
        GPIO.output(GREEN_PIN_2, GPIO.LOW)
        print("[RGB2] BLUE")
    elif value == 2:
        GPIO.output(RED_PIN_2, GPIO.HIGH)
        GPIO.output(BLUE_PIN_2, GPIO.LOW)
        GPIO.output(GREEN_PIN_2, GPIO.LOW)
        print("[RGB2] RED")

def cleanup():
    GPIO.output(RED_PIN_1, GPIO.LOW)
    GPIO.output(BLUE_PIN_1, GPIO.LOW)
    GPIO.output(GREEN_PIN_1, GPIO.LOW)
    GPIO.output(RED_PIN_2, GPIO.LOW)
    GPIO.output(BLUE_PIN_2, GPIO.LOW)
    GPIO.output(GREEN_PIN_2, GPIO.LOW)
    GPIO.cleanup()
