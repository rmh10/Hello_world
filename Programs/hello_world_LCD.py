import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()

while True:
	mylcd.lcd_display_string("Hello World!", 1, 2)
# 1 is the row of choice and 2 is the column of choice