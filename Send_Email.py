import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromadd = "From Address" 
toadd = "To Address"
password = "Pasword"

msg = MIMEMultipart()
msg['From'] = fromadd
msg['To'] = toadd
msg['Subject'] = "Test Email using Python"

body = "Hey! This email was sent from your terminal\n"

important = "The Oil in the transfromer is low\nSend assistance now!\n" 
msg.attach(MIMEText(important, 'plain'))

filename = "ADC_program.py"
attachment = open("Sensors/pressure_sensor/pressure_sensor.py","rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" %filename)

msg.attach(part)

def send_1():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(fromadd, password)
    text = msg.as_string()
    server.sendmail(fromadd, toadd, text)
    server.quit()

def sendIfTrue():
    #for i in range(0,10): 
     i = raw_input("Input 0 for Oil High and input any other number for Oil Low\n")
     if (i == 0):
         outMsg = "Oil level = HIGH"
     else:
         outMsg = "Oil level = LOW"
         send()
     print("Iteration= %i" %i)

try:
    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #server.ehlo()
    #server.login(fromadd, password)
    #text = msg.as_string()
    #server.sendmail(fromadd, toadd, text)
    #server.quit()
    sendIfTrue()
    print ("Successfully sent your email!\n")

except:
    print("Sending did not complete")
