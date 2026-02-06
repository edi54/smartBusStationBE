import RPi.GPIO as GPIO

RAIN_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

_prev_state = None  

def read_rain():
    global _prev_state
    rain_detected = GPIO.input(RAIN_PIN)
    current_state = True if rain_detected == GPIO.LOW else False
    
    if current_state != _prev_state:
        _prev_state = current_state
        print("Raining" if current_state else "NOT Raining")
    
    return current_state  
