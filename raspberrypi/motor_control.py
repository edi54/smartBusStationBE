import RPi.GPIO as GPIO
import time
import os
from firebase_admin import db

PWM_PIN_1 = 12
DIR_PIN_1 = 6
PWM_PIN_2 = 19
DIR_PIN_2 = 16

_last_state = 0
_last_manual_state = 0

pwm1 = None
pwm2 = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def setup():
    global pwm1, pwm2
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_PIN_1, GPIO.OUT)
    GPIO.setup(DIR_PIN_1, GPIO.OUT)
    GPIO.setup(PWM_PIN_2, GPIO.OUT)
    GPIO.setup(DIR_PIN_2, GPIO.OUT)

    pwm1 = GPIO.PWM(PWM_PIN_1, 100)
    pwm2 = GPIO.PWM(PWM_PIN_2, 50)
    pwm1.start(0)
    pwm2.start(0)

def play_sound(filename):
    filepath = os.path.join(BASE_DIR, filename)
    os.system(f"aplay -D plughw:4,0 {filepath} > /dev/null 2>&1")

def check_and_update_motor():
    global _last_state
    motor_ref = db.reference('motor')
    state = motor_ref.get()

    if state != _last_state:
        _last_state = state
        _run_motor(state, mode='auto')

def check_and_update_motor_manual():
    global _last_manual_state
    manual_ref = db.reference('manual_motor')
    state = manual_ref.get()

    if state != _last_manual_state:
        _last_manual_state = state
        _run_motor(state, mode='manual')

def _run_motor(state: int, mode='auto'):
    if state == 1:
        print(f"opening ({mode})")

        if mode == 'manual':
            play_sound("manual_open.wav")
        else:
            play_sound("auto_open.wav")

        time.sleep(1)

        GPIO.output(DIR_PIN_1, GPIO.LOW)
        GPIO.output(DIR_PIN_2, GPIO.LOW)
        pwm1.ChangeDutyCycle(70)
        pwm2.ChangeDutyCycle(70)
        time.sleep(2.5)
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)

    elif state == 0:
        print(f"closing ({mode})")

        if mode == 'manual':
            play_sound("manual_close.wav")
        else:
            play_sound("auto_close.wav")

        time.sleep(1)

        GPIO.output(DIR_PIN_1, GPIO.HIGH)
        GPIO.output(DIR_PIN_2, GPIO.HIGH)
        pwm1.ChangeDutyCycle(75)
        pwm2.ChangeDutyCycle(70)
        time.sleep(2.5)
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)

def sync_manual_state():
    global _last_manual_state
    _last_manual_state = _last_state

def sync_auto_state():
    global _last_state
    _last_state = _last_manual_state

def cleanup():
    if pwm1:
        pwm1.stop()
    if pwm2:
        pwm2.stop()
    GPIO.cleanup()
