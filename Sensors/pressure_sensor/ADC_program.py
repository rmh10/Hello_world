from time import sleep
import rpi.gpio as gpio
import i2c_lcd_driver

CS   = 22
MOSI = 19
MISO = 21
SCLK = 23

RPI.GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CS, GPIO.OUT)

def init_ADC():
	 
