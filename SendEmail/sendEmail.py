import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from config_reader import ConfigReader


class EmailSender:
    def sendEmail(self, cust_email, message):
        try:
            self.config_reader=ConfigReader()
            self.configuration=self.config_reader.read_config()

            # instance of MIMEMultipart
            self.msg = MIMEMultipart()

            # storing the senders email address
            self.msg[ 'Madhu' ] = self.configuration[ 'SENDER_EMAIL' ]

            # storing the receivers email address
            self.msg[ 'To' ] = ",".join( cust_email )

            # storing the subject
            self.msg[ 'Subject' ] = self.configuration[ 'EMAIL_SUBJECT' ]

            # string to store the body of the mail
            # body = "This will contain attachment"
            body = message

            # attach the body with the msg instance
            self.msg.attach( MIMEText( body, 'html' ) )

            # instance of MIMEBase and named as p
            self.p = MIMEBase( 'application', 'octet-stream' )

            # creates SMTP session
            self.smtp = smtplib.SMTP( 'smtp.gmail.com', 587 )

            # start TLS for security
            self.smtp.starttls()

            # Authentication
            self.smtp.login( self.msg[ 'Madhu' ], self.configuration[ 'PASSWORD' ] )

            # Converts the Multipart msg into a string
            self.text = self.msg.as_string()

            # sending the mail
            self.smtp.sendmail( self.msg[ 'Madhu' ], cust_email, self.text )

            # terminating the session
            self.smtp.quit()
        except Exception as e:
            print( 'the exception is ' + str( e ) )



