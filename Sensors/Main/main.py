# File Name: main.py
# Author: Roy Helms
# Date Created: 04/12/2018
# Date Last Modified: 4/12/2018
# Python Version: 2.7 
#
# Description:
#     This file contains the main instructions for the
#     monitoring system inculding the following functions:
#
# 1. Taking readings of oil level, pressure, and temperature
# 2. Taking readings every minute
# 3. Building a file that will display the time and value of the readings
# 4. Send and email with the file build attached to it


import os
import glob
import time
#import smbus
import smtplib
import email
import I2C_LCD_driver
import temperature_sensor_code
import oil_level_sensor
from time import sleep

display = I2C_LCD_driver.lcd()

#from email.MIMEMultipart import MIMEMulitpart
#from email.MIMEText import MIMEText

#print (time.strftime("Time is: %H:%M:%S"))

# 1. Function to take readings from each sensor
def read_sensors():
	while true:
		print (time.strftime("Time is: %H:%M:%S"))
		sleep(2.5)
		read_level()
		sleep(2.5)
		read_temp()
		sleep(2.5)
		print("Starting next reading.")
	
# 2. Function to output to the LCD


# 3. Function to store readings into a file
#def buildFile(level, temperature, pressure)


try:
    while True:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(float, GPIO.IN)
        read_sensors()
	GPIO.cleanup()

except KeyboardInterrupt:
    print "Cleaning"
    display.lcd_display_string("              ")
    GPIO.cleanup()try:
    while True:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(float, GPIO.IN)
        read_level()
        GPIO.cleanup()

