import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import utils


class MailSender:

    def __init__(self):
        self.smtp_ssl_host = utils.read_config_value('STANDARD', 'server_smtp')
        self.smtp_ssl_port = utils.read_config_value('STANDARD', 'porta_server')
        self.username = utils.read_config_value('STANDARD', 'email')
        self.password = utils.read_config_value('STANDARD', 'password')
        self.sender = utils.read_config_value('STANDARD', 'email')

        self.smtp_ssl_host_pec = utils.read_config_value('PEC', 'server_smtp')
        self.smtp_ssl_port_pec = utils.read_config_value('PEC', 'porta_server')
        self.username_pec = utils.read_config_value('PEC', 'email')
        self.password_pec = utils.read_config_value('PEC', 'password')
        self.sender_pec = utils.read_config_value('PEC', 'email')

        self._month = None
        self._year = None

    # send mail with standard mail address
    def send_mail(self, receiver, pdf_list):
        print("sending standard mail to: " + receiver)

        body = utils.read_mail_content()

        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = receiver
        message['Subject'] = utils.read_subject_content() + ' ' + self._month + ' ' + self._year

        message.attach(MIMEText(body, 'plain'))

        message = self.add_attachments(message, pdf_list)

        server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)
        server.login(self.username, self.password)

        text = message.as_string()
        server.sendmail(self.sender, receiver, text)
        server.quit()

        print("mail inviata!")

    # send mail with pec address
    def send_mail_pec(self, receiver, pdf_list):
        print("sending pec mail to: " + receiver)

        body = utils.read_mail_content()

        message = MIMEMultipart()
        message['From'] = self.sender_pec
        message['To'] = receiver
        message['Subject'] = utils.read_subject_content() + self._month + ' ' + self._year

        message.attach(MIMEText(body, 'plain'))

        message = self.add_attachments(message, pdf_list)

        server = smtplib.SMTP_SSL(self.smtp_ssl_host_pec, self.smtp_ssl_port_pec)
        server.login(self.username_pec, self.password_pec)

        text = message.as_string()
        server.sendmail(self.sender_pec, receiver, text)
        server.quit()

        print("mail inviata!")

    @staticmethod
    def add_attachments(message, pdf_list):
        attachments_list = "allego i seguenti file: "
        for pdf in pdf_list:
            attachments_list += pdf + ","

            pdf_path = utils.read_config_value('PATH', 'path_to_send') + pdf

            # open the file in binary
            binary_pdf = open(pdf_path, 'rb')

            payload = MIMEBase('application', 'octate-stream', Name=pdf)
            payload.set_payload(binary_pdf.read())

            # encoding the binary into base64
            encoders.encode_base64(payload)

            # add header with pdf name
            payload.add_header('Content-Decomposition', 'attachment', filename=pdf)
            message.attach(payload)
        print(attachments_list)
        return message

    def set_month(self, month):
        self._month = month

    def set_year(self, year):
        self._year = year
