import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
from DjangoDRF import settings

msg = MIMEMultipart()
server = smtplib.SMTP(settings.AUTH_DOMAIN, 587)


class ClassSendEmail():
    def __init__(self, email_data):
        self.recipient_list = email_data.get("recipient_list")
        self.email_body = email_data.get("email_body")
        self.email_subject = email_data.get("email_subject")


    def SendEmail(self):
        print(f"{self.recipient_list}, {self.email_body}, {self.email_subject}")
        try:

            msg['From'] = f"Amit Jamwal <{settings.AUTH_EMAIL}>"
            # msg['To'] = ", ".join( self.recipient_list )
            msg['Subject'] = self.email_subject
            msg.attach( MIMEText( self.email_body, 'html' ) )

            server.starttls()
            server.login( settings.AUTH_EMAIL, settings.AUTH_EMAIL_PWD )
            text = msg.as_string()
            # server.sendmail(settings.AUTH_EMAIL, self.recipient_list, text)

            for email in self.recipient_list:
                msg['To'] = email
                server.sendmail( settings.AUTH_EMAIL, email, text )


            server.quit()
            return "success"
        except:
            traceback.print_exc()
            return None


