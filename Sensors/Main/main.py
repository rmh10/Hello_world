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
# 

import os
import glob
import time
import smbus
import smtplib
import email
import I2C_LCD_driver
import temperature_sensor_code
import oil_level_sensor

#from email.MIMEMultipart import MIMEMulitpart
#from email.MIMEText import MIMEText


