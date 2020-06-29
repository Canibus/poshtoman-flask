from ..config import Config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_to(email, value):
    msg = MIMEMultipart()
    msg['From'] = Config.MAIL_LOGIN
    msg['Subject'] = 'Восстановление пароля'
    msg['To'] = email
    msg.attach(MIMEText(value, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(Config.MAIL_LOGIN, Config.MAIL_PASSWORD)
    server.send_message(msg)
    msg = None
    server.quit()