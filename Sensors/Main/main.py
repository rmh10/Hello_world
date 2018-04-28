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

#!/usr/bin/python
import os
import glob
import time
import datetime
#import smbus
import smtplib
import spidev
import binascii
import email
import RPi.GPIO as GPIO 
import I2C_LCD_driver
#import temperature_sensor_code
#import oil_level_sensor
from time import sleep
#from Send_Email_test import send
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
f_switch = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(optical, GPIO.IN)
GPIO.setup(f_switch, GPIO.IN)

fromadd = "From Address"
toadd = "To Address"
password = "Password"

#### 1. Function to take readings from each sensor ####

def read_optical_level():
    outMsg_optical = ""
    if GPIO.input(optical) == 0:
        outMsg_optical = "Op level = HIGH     "
    if GPIO.input(optical) == 1:
        #while GPIO.input(optical) == 0:
        outMsg_optical = "Op level = LOW     "
        msg_LL = "LL"
        choose_msg(msg_LL)
            #time.sleep(10)
            #display.lcd_display_string(outMsg_optical)

    info = open("sensor_info.txt", 'a')
    info.write(outMsg_optical + "\n")
    info.close()
    
    display.lcd_display_string(outMsg_optical)


def read_float_level(): 
    outMsg_float = ""
    if GPIO.input(f_switch) == 0:
        outMsg_float = "Fl level = HIGH     "
    if GPIO.input(f_switch) == 1:
        #while GPIO.input(f_switch) == 1:
        outMsg_float = "Fl level = LOW     "
        msg_LL = "LL"
        choose_msg(msg_LL)
            #time.sleep(10)
            #display.lcd.display.string(outMsg_float)
    
    info = open("sensor_info.txt", 'a')
    info.write(outMsg_float + "\n")
    info.close()
    
    display.lcd_display_string(outMsg_float)


def read_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    #if lines[0].strip90[-3:] != 'YES':
    time.sleep(0.2)
    equals_pos = lines[1].find('t=')
    #if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    
    info = open("sensor_info.txt", 'a')
    info.write("Temp(F)= %.2f\n" %temp_f)
    info.close()    
	
    if (temp_f < 40.0):
        msg_TL = "TL"
        choose_msg(msg_TL)
    elif (temp_f > 120.0):
        msg_TH = "TH"
        choose_msg(msg_TH)
    display.lcd_display_string("Temp(F): %.2f     " %temp_f)
        #time.sleep(2.5)
 	#display.lcd_display_string("Temp(C): %s" %temp_c)


def read_pres(adc):
    assert 0 <= adc <= 1
    
    if adc:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000

    resp = spi.xfer2([1,cbyte,0])
    return((resp[1] & 31) << 6) + (resp[2] >> 2)


def read_sensors():
    today = datetime.date.today()
    start_info = open("sensor_info.txt", 'w')
    start_info.write(today.strftime("This file contains the sensor information from %m %d, %Y\n"))
    start_info.close() 
    while True:
        display.lcd_display_string(time.strftime("Time= %H:%M:%S     "), 1, 0)
        display.lcd_display_string(today.strftime("Date= %m/%d/%Y     "), 2, 0)

        info = open("sensor_info.txt", 'a')
        info.write(time.strftime("\nTime= %H:%M:%S\n"))
        info.close()
	sleep(2.5)

        display.lcd_clear()	
        read_optical_level()
        sleep(2.5)
        read_float_level()
        sleep(1.25)
         	
        read_temp()
	sleep(2.5)
       
        adc = 0 
        adcData = read_pres(adc) 
        voltage = round(((adcData * 5000) / 1024),0)
        pressure = round(((250/4000) * voltage) - (250/8000))
        display.lcd_display_string("Pres(Psi): %.2f     " %pressure)

        info = open("sensor_info.txt", 'a')
        info.write("Pres(Psi)= %.2f\n" %pressure)
        info.close()
        
        if (pressure < -10):
            msg_PL = "PL"
            choose_msg(msg_PL)
        elif (pressure > 50):
            msg_PH = "PH"
            choose_msg(msg_PH)
        sleep(2.5)
	
#### 2. Function to send emails ####

def choose_msg(message):
    #message = getMsg(choose_in)
    if (message == "LH"):
        subject = "Oil level is too HIGH"
        body = ("Time: %s\n\nOil level is too HIGH. Assistance is needed!" %time.strftime("%H:%M:%S"))
  
    elif (message == "LL"):
        subject = "Oil level is too LOW"  
        body = ("Time: %s\n\nOil level is too LOW. Assistance is needed!" %time.strftime("%H:%M:%S"))  
    
    elif (message == "TH"):
        subject = "Temperture is too HIGH"
        body = ("Time: %s\n\nTemperature is too HIGH. Assistance is needed!" %time.strftime("%H:%M:%S"))
    
    elif (message == "TL"):
        subject = "Temperture is too LOW"
        body = ("Time: %s\n\nTemperature is too LOW. Assistance is needed!" %time.strftime("%H:%M:%S")) 
    
    elif (message == "PH"): 
        subject = "Pressure is too HIGH"
        body = ("Time: %s\n\nPressure is too HIGH. Assistance is needed!" %time.strftime("%H:%M:%S"))   
    
    elif (message == "PL"): 
        subject = "Pressure is too LOW"
        body = ("Time: %s\n\nPressure is too LOW. Assistance is needed!" %time.strftime("%H:%M:%S"))  

    else:
        subject = "Emergency message"
        body = "Incorrect message received from 'choose_msg()' function in main.py"
    send_emails(subject, body) 
    

def send_emails(sub, bod):
    msg = MIMEMultipart()
    msg['From'] = fromadd
    msg['To'] = toadd
    msg['Subject'] = sub
    
    msg.attach(MIMEText(bod, 'plain'))

    filename = "sensor_info.pdf"
    attachment = open("sensor_info.txt", "rb")
     
    part = MIMEBase('application', 'octet_stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment: filename= %s" %filename)
      
    msg.attach(part)
     
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(fromadd, password)
    text = msg.as_string()
    server.sendmail(fromadd, toadd, text)
    server.quit() 


#### 3. Function to store readings into a file ####
#def buildFile(level, temperature, pressure)


try:
    #while True:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(optical, GPIO.IN)
        GPIO.setup(f_switch, GPIO.IN)
        read_sensors()
	#GPIO.cleanup()

except KeyboardInterrupt:
    print "Cleaning"
    display.lcd_display_string("              ")
    GPIO.cleanup()
