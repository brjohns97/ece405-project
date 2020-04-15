from pprp import app
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os.path
import emailinformation

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

email = emailinformation.piemail
password = emailinformation.pipassword
send_to_email = emailinformation.myemail
subject = 'Raspberry Pi IP Adress and Port Number'
ip = get_ip_address()
message = 'The URL is %s:8000' % (ip)

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(message,'plain'))

server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.login(email,password)
text = msg.as_string()
server.sendmail(email,send_to_email,text) #will show up in spam, mark as not spam
#for another person server.sendmail(email,send_to_email,text) #will show up in spam, mark as not spam

server.close()

if __name__ == "__main__":
    app.run(debug=True, host=get_ip_address(), port=8000)
    
