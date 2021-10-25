import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import path_utils
import utils
import logging


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

    def sent_pdf_list_to_customer(self, code, customer_email, mail_type, pdf_list):
        try:
            # check mail type
            if mail_type == "Falso":
                self._send_mail(customer_email, pdf_list)
            elif mail_type == "Vero":
                self._send_mail_pec(customer_email, pdf_list)
            else:
                raise ValueError("Can't read mail type value!")
            # Move pdf file to "sent" folder
            utils.move_pdf_to_sent_folder(pdf_list)
        except ValueError:
            logging.warning("Error decoding " + utils.read_config_value('PATH', 'clients_filename') +
                            " for client " + code+"\n")

    # send mail with standard mail address
    def _send_mail(self, receiver, pdf_list):
        logging.info("sending standard mail to: " + receiver)

        body = utils.read_mail_content()

        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = receiver
        message['Subject'] = utils.read_subject_content() + ' ' + self._month + ' ' + self._year

        message.attach(MIMEText(body, 'plain'))

        message = self._add_attachments(message, pdf_list)

        server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)
        server.login(self.username, self.password)

        text = message.as_string()
        server.sendmail(self.sender, receiver, text)
        server.quit()

        logging.info("mail inviata!\n")

    # send mail with pec address
    def _send_mail_pec(self, receiver, pdf_list):
        logging.info("sending pec mail to: " + receiver)

        body = utils.read_mail_content()

        message = MIMEMultipart()
        message['From'] = self.sender_pec
        message['To'] = receiver
        message['Subject'] = utils.read_subject_content() + self._month + ' ' + self._year

        message.attach(MIMEText(body, 'plain'))

        message = self._add_attachments(message, pdf_list)

        server = smtplib.SMTP_SSL(self.smtp_ssl_host_pec, self.smtp_ssl_port_pec)
        server.login(self.username_pec, self.password_pec)

        text = message.as_string()
        server.sendmail(self.sender_pec, receiver, text)
        server.quit()

        logging.info("mail sent!\n")

    @staticmethod
    def _add_attachments(message, pdf_list):
        attachments_list = "attaching pdf: "
        for pdf in pdf_list:
            attachments_list += pdf + ","

            pdf_path = os.path.join(path_utils.get_to_send_folder_path(), pdf)

            # open the file in binary
            binary_pdf = open(pdf_path, 'rb')

            payload = MIMEBase('application', 'octate-stream', Name=pdf)
            payload.set_payload(binary_pdf.read())

            # encoding the binary into base64
            encoders.encode_base64(payload)

            # add header with pdf name
            payload.add_header('Content-Decomposition', 'attachment', filename=pdf)
            message.attach(payload)
        logging.info(attachments_list)
        return message

    def set_month(self, month):
        self._month = month

    def set_year(self, year):
        self._year = year
