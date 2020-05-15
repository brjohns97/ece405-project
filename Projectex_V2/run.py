from pprp import app
import socket
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import os.path
import emailinformation

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

fromaddr = emailinformation.piemail
toaddr = emailinformation.email_list
myPassword = emailinformation.pipassword

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ','.join(toaddr)
msg['Subject'] = 'Raspberry Pi IP Adress and Port Number'
ip = get_ip_address()
body = 'The URL is %s:8000' % (ip)
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, myPassword)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()


if __name__ == "__main__":
    app.run(debug=False, host=get_ip_address(), port=8000)
    
