import utime

import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from rtc_sdCard import get_Time


i2c = I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)
devices = i2c.scan()

if len(devices) == 0:
    print("No I2C devices found")
else:
    I2C_ADDR = devices[0]
    #print(f"Found I2C device at address: {hex(I2C_ADDR)}")


I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)



# Text wih current time
def text(message):
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(message)
    
    lcd.move_to(11,1)
    lcd.putstr(get_Time())
    return message
    

