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
            if mail_type == "Falso" or mail_type == "Vero":
                self._send_mail(customer_email, mail_type, pdf_list)
            else:
                raise ValueError("Can't read mail type value!")
            # Move pdf file to "sent" folder
            utils.move_pdf_to_sent_folder(pdf_list)
        except ValueError:
            logging.warning("Error decoding " + utils.read_config_value('PATH', 'clients_filename') +
                            " for client " + code+"\n")

    # send mail with standard mail address
    def _send_mail(self, receiver, mail_type, pdf_list):
        logging.info("sending standard mail to: " + receiver)

        body = utils.read_mail_content()

        sender_by_mail_type = self._get_sender_by_mail_type(mail_type)
        message = self._build_message(receiver, sender_by_mail_type)
        message.attach(MIMEText(body, 'plain'))
        message = self._add_attachments(message, pdf_list)

        server = self._build_server(mail_type)

        text = message.as_string()
        server.sendmail(sender_by_mail_type, receiver, text)
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

    def _get_sender_by_mail_type(self, mail_type):
        if mail_type == "False":
            sender_by_mail_type = self.sender
        else:
            sender_by_mail_type = self.sender_pec
        return sender_by_mail_type

    def _build_message(self, receiver, sender):
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = utils.read_subject_content() + ' ' + self._month + ' ' + self._year
        return message

    def _build_server(self, mail_type):
        if mail_type == "Falso":
            host = self.smtp_ssl_host
            port = self.smtp_ssl_port
            username = self.username
            psw = self.password
        else:
            host = self.smtp_ssl_host_pec
            port = self.smtp_ssl_port_pec
            username = self.username_pec
            psw = self.password_pec
        try:
            server = smtplib.SMTP_SSL(host, port)
            server.login(username, psw)
        except smtplib.SMTPAuthenticationError:
            logging.error("Email authentication failed!\n")
            utils.end_execution()
        except Exception:
            logging.error("Error connecting to email server, check internet connection or smtp parameters!\n")
            utils.end_execution()
        return server

    def set_month(self, month):
        self._month = month

    def set_year(self, year):
        self._year = year
