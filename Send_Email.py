import smtplib

from email.MIMEMultipart import Multipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromadd = [From Email]
toadd = [To Email]
password = [Instert Password]

msg = MIMEMultipart()
msg['From'] = fromadd
msg['To'] = toadd
msg['Subject'] = "Test Email using Python"

body = "Hey Roy! This email was sent from your terminal\n"
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromadd, password)
text = msg.as_string()
smtpObj.sendmail(fromadd, toadd, text)
server.quit()
print ("Successfully sent your email!\n")
