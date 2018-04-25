# File Name: main.py
# Author: Roy Helms
# Date Created: 04/12/2018
# Date Last Modified: 4/24/2018
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
import spidev
import binascii
import email
import rpi.gpio as gpio
import I2C_LCD_driver
import temperature_sensor_code
import oil_level_sensor
from time import sleep
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 250000

display = I2C_LCD_driver.lcd()

optical = 16
float = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(optical, GPIO.IN)
GPIO.setup(float, GPIO.IN)

fromadd = "From Address"
toadd = "To Address"


#### 1. Function to take readings from each sensor ####

def read_optical_level():
    elif GPIO.input(optical) == 0:
        while GPIO.input(optical) == 0:
            outMsg_optical = "Oil level = LOW"
            email_sub, email_bod = choose_msg("LL")
            send_email_vital()
            time.sleep(10)
            display.lcd_display_string(outMsg_optical)
    display.lcd_display_string(outMsg_optical)


def read_float_level(): 
    if GPIO.input(float) == 0:
        outMSG_float = "Oil level = HIGH"
    elif GPIO.input(float) == 1:
        while GPIO.input(float) == 1:
            outMsg_float = "Oil level = LOW"
            send_email_vital(important)
            time.sleep(10)
            display.lcd.display.string(outMsg_float)
    display.lcd.display.string(outMsg_float)


def read_temp():
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


def read_pres(adc):
    assert 0 <= adc <= 1
    
    if adc:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000

    resp = spi.xfer2([1,cbyte,0])
    return((r[1] & 31) << 6) + (r[2] >> 2)


def read_sensors():
    #while True:
        adc = 0
        
        display.lcd_display_string(time.strftime("Time: %H:%M:%S"))
	sleep(2.5)
	
        read_level()
	sleep(2.5)
         	
        read_temp()
	sleep(2.5)
        
        adcData = read_pres(adc) 
        voltage = round(((adcData * 4500) / 1024),0)
        pressure = round((voltage / 4500) *450) 
        display.lcd_display_string("Pressure(Psi): %s" %pressure)
        
        if (pressure < 20)
            choose_msg("PH")
        sleep(2.5)
	
#### 2. Function to send emails ####

def choose_msg(message)
    #message = getMsg(choose_in)
    if (message == "Level High"):
        subject = "Oil level is too HIGH"
        body = ("Time: %s\n\nOil level is too HIGH. Assistance is needed!" %time.strftime("%H:%M:%S"))
  
    elif (message == "Level Low"):
        subject = "Oil level is too HIGH"  
        body = ("Time: %s\n\nOil level is too LOW. Assistance is needed!" %time.strftime("%H:%M:%S"))  
    
    elif (message == "Temp High"):
        subject = "Temperture is too HIGH"
        body = ("Time: %s\n\nTemperature is too HIGH. Assistance is needed!" %time.strftime("%H:%M:%S"))
    
    elif (message == "Temp Low"):
        subject = "Temperture is too LOW"
        body = ("Time: %s\n\nTemperature is too LOW. Assistance is needed!" %time.strftime("%H:%M:%S")) 
    
    elif (message == "Pres High"): 
        subject = "Pressure is too HIGH"
        body = ("Time: %s\n\nPressure is too HIGH. Assistance is needed!" %time.strftime("%H:%M:%S"))   
    
    elif (message == "Pres Low"): 
        subject = "Pressure is too LOW"
        body = ("Time: %s\n\nPressure is too LOW. Assistance is needed!" %time.strftime("%H:%M:%S"))  

    else:
        subject = "Emergency message"
        body = "Incorrect message received from "getMsg()" function in main.py"
   return(subject, body) 

def getMsg(choice):
    if (choice == "LH"):
        msg = "Level High"
    elif (choice == "LL"):
        msg = "Level Low"
    elif (choice == "TH"):
        msg = "Temp High"
    elif (choice == "TL")
        msg = "Temp Low"
    elif (choice == "PH")
        msg = "Pres High"
    elif (choice == "PL")
        msg = "Pres Low"
    else:
        msg = "No message"
    return msg

def send_emails():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(fromadd, password)
    text = msg.as_string()
    server.sendmail(fromadd, toadd, text)
    server.quit() 


#### 3. Function to store readings into a file ####
#def buildFile(level, temperature, pressure)


msg = MIMEMultipart()
msg['From'] = fromadd
msg['To'] = toadd
msg['Subject'] = 

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
