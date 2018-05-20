import configparser
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


USERNAME, PASSWORD, SMTP_HOST, SMTP_PORT = None, None, None, None


def settings_init(path="", set_file="settings.secret"):
    """update settings from settings.secret"""
    config = configparser.ConfigParser()
    config.read(set_file)
    global SMTP_HOST, SMTP_PORT, USERNAME, PASSWORD
    SMTP_HOST = config["mail"]["SMTPhost"]
    SMTP_PORT = config["mail"]["SMTPport"]
    USERNAME = config["mail"]["Mail"]
    PASSWORD = config["mail"]["Password"]


def send_mail(target_mail, path, file_name):
    mail_text = "Hi! It's your report from YourSecReport."
    mail_subject = "Report from YourSecReport"
    mail_sender = "report@yousecreport.com"

    msg = MIMEMultipart('TEST')
    msg["Subject"] = mail_subject
    msg["From"] = mail_sender
    msg["To"] = target_mail

    txt_mail = MIMEText(mail_text)
    msg.attach(txt_mail)

    path_to_file = os.path.join(path, file_name)
    with open(path_to_file, 'rb') as fp:
        pdf_file = MIMEApplication(fp.read(), "pdf")
        pdf_file.add_header('Content-Disposition', 'attachment', filename='report.pdf')
        msg.attach(pdf_file)

    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    server.login(USERNAME, PASSWORD)
    server.sendmail(mail_sender, target_mail, msg.as_string())
    server.quit()


settings_init()
