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

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

display = I2C_LCD_driver.lcd()

#from email.MIMEMultipart import MIMEMulitpart
#from email.MIMEText import MIMEText

#print (time.strftime("Time is: %H:%M:%S"))

# 1. Function to take readings from each sensor

def temp_reading():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    if lines[0].strip90[-3:] != 'YES':
        time.sleep(0.2)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        display.lcd_display_string("Temp(F): %s" %temp_f)
        time.sleep(2.5)
 	display.lcd_display_string("Temp(C): %s" %temp_c)

def level_reading():
   outMsg = "No message yet"
   if GPIO.input(float) 

def read_sensors():
    while True:
        display.lcd_display_string(time.strftime("Time is: %H:%M:%S"))
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
    GPIO.cleanup()
