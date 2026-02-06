import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn


i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)
ads.mode = 0  
ads.gain = 1 

chan = AnalogIn(ads, 0)

_prev_wind_speed = None

def read_wind():
    global _prev_wind_speed

    voltage = chan.voltage
    wind_speed = (voltage - 0.07) * (70 / (1.4 - 0.07))
    wind_speed = max(0, min(wind_speed, 50))
    wind_speed = int(wind_speed)

    if wind_speed != _prev_wind_speed:
        print(f"Wind speed changed: {wind_speed} m/s")
        _prev_wind_speed = wind_speed
        return wind_speed
    return None
