#import socket
#import fcntl
#import struct
import subprocess
import I2C_LCD_driver
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell = True )
print str(IP)

display = I2C_LCD_driver.lcd()
display.lcd_display_string(IP)

#def get_ip_address(ifname):
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #return socket.inet_ntoa(fcntl.ioctl(
        #s.fileno(),
        #0x8915, 
        #struct.pack('256s', ifname[:15])
    #)[20:24])

#mylcd.lcd_display_string("IP Address:", 1) 

#mylcd.lcd_display_string(get_ip_address('wlan0'), 2)
