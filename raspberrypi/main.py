import threading
import time
from firebase_admin import credentials, initialize_app, db
import RPi.GPIO as GPIO

import rain_sensor
import motor_control
import led_control
import rgb_led
#import wind_sensor
#from streaming import create_app
#from stt import stt_button_listener 
#from call import start_call_monitor

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

cred = credentials.Certificate("smart-bus-station-325771-firebase-adminsdk-fbsvc-ed6a9fd6f8.json")
initialize_app(cred, {
    'databaseURL': 'https://smart-bus-station-325771-default-rtdb.firebaseio.com/'
})

#app = create_app()

def sensor_loop():
    ref_manual = db.reference('manual')
    #ref_wind_sensor = db.reference('wind_sensor')
    ref_rain_sensor = db.reference('rain_sensor')

    rgb_led.setup()
    motor_control.setup()
    led_control.setup()

    was_manual = False

    try:
        while True:
            rain_state = rain_sensor.read_rain()
            if rain_state is not None:
                ref_rain_sensor.set(rain_state)

            #wind_speed = wind_sensor.read_wind()
            #if wind_speed is not None:
                #print(f"Uploading wind speed to Firebase: {wind_speed} m/s")
                #ref_wind_sensor.set(wind_speed)

            is_manual = ref_manual.get()

            if is_manual != was_manual:
                if is_manual:
                    motor_control.sync_manual_state()
                else:
                    motor_control.sync_auto_state()
                was_manual = is_manual

            if is_manual:
                

                motor_control.check_and_update_motor_manual()

                manual_led = db.reference('manual_led').get()
                manual_chair_1 = db.reference('manual_chair_1').get()
                manual_chair_2 = db.reference('manual_chair_2').get()

                led_control.set_led(manual_led if manual_led is not None else False)
                rgb_led.update_led_1(manual_chair_1 if manual_chair_1 is not None else 0)
                rgb_led.update_led_2(manual_chair_2 if manual_chair_2 is not None else 0)

            else:
                motor_control.check_and_update_motor()
                led_control.update_led()

                chair_1 = db.reference('chair_1').get()
                chair_2 = db.reference('chair_2').get()
                rgb_led.update_led_1(chair_1)
                rgb_led.update_led_2(chair_2)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Terminated by user.")
    except Exception as e:
        print(f"[ERROR] sensor_loop exception: {e}")
    finally:
        GPIO.cleanup()
        rgb_led.cleanup()

if __name__ == "__main__":
    threading.Thread(target=sensor_loop, daemon=True).start()
    #threading.Thread(target=stt_button_listener, daemon=True).start()
    #threading.Thread(target=start_call_monitor, daemon=True).start()

   #app.run(host='0.0.0.0', port=8080)
