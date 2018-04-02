from time import sleep
import RPi.GPIO as GPIO

led = 22
float = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(float, GPIO.IN)
GPIO.setup(led,GPIO.OUT)

while True:
	if GPIO.input(float) == 1:
		GPIO.output(led, False)
		#outMsg = "Oil level is HIGH"
		sleep(.1)
	if GPIO.input(float) == 0:
		GPIO.output(led, True)
		#outMsg = "Oil level is LOW"
#print outMsg

GPIO.cleanup()
