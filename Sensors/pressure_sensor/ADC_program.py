from time import sleep
import rpi.gpio as gpio
import i2c_lcd_driver
import spidev

#CE0  = 24
#MOSI = 19
#MISO = 21
#SCLK = 23

#RPI.GPIO
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(CS, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,1)

def init_ADC():
    GPIO.out(CS, True)

