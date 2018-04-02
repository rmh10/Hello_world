from time import sleep
import RPi.GPIO as GPIO
import I2C_LCD_driver

led = 22
float = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(float, GPIO.IN)
#GPIO.setup(led,GPIO.OUT)

display = I2C_LCD_driver.lcd()

def writedisp():
    sleep (1)
    outMsg = "No message yet"
    if GPIO.input(float) == 1:
	    #GPIO.output(led, False)
	    outMsg = "Oil level=LOW  "
	    sleep(.1)
    if GPIO.input(float) == 0:
	    #GPIO.output(led, True)
            outMsg = "Oil level=HIGH"
    print outMsg
    display.lcd_display_string(outMsg)

try:
    while True:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(float, GPIO.IN)
        writedisp()
        GPIO.cleanup()

except KeyboardInterrupt:
    print "Cleaning"
    display.lcd_display_string("              ")
    GPIO.cleanup()
