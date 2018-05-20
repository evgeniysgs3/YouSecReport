# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

from ReadConfig import Config


class EmailSender:

    def __init__(self):
        self.__server = smtplib.SMTP("smtp.gmail.com", 587)

    def send_report(self, email, file_report):
        """Send report to customer"""

        config = Config()
        login, passwd = config.get_auth_for_send_email()

        with open(file_report) as fr:
            # Create a text/plain message
            msg = MIMEText(fr.read())

        msg['Subject'] = 'The contents of %s' % file_report
        msg['From'] = login
        msg['To'] = email

        # Send the message via our own SMTP server.
        try:
            self.__server.ehlo()
            self.__server.starttls()
            self.__server.login(login, passwd)
            self.__server.send_message(msg)
        except Exception as e:
            print('Error: {}'.format(e))
        finally:
            self.__server.quit()


if __name__ == "__main__":
    report = EmailSender()
    report.send_report('actionnum@protonmail.com', 'test.txt')
