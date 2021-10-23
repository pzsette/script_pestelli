import extractor
from mail_sender import *
import logging

if __name__ == '__main__':

    mail_sender = MailSender()

    # ask user month and year
    date = utils.get_date_info()

    if date is not None:
        # assign to mail_sender
        mail_sender.set_month(date[0])
        mail_sender.set_year(date[1])

        # Group pdf files by their code "007: {1.pdf, 2.pdf, 3.pdf}, 002: {4.pdf},..."
        pdf_files_by_code = extractor.scan_pdfs()
        # Perform this routine for every code
        for code_group in pdf_files_by_code.items():
            code = code_group[0]
            try:
                # get email address associated to this code and mail type
                emails_info = extractor.find_emails(code)
                try:
                    # check mail type
                    if emails_info[1] == "Falso":
                        mail_sender.send_mail(emails_info[0], code_group[1])
                    elif emails_info[1] == "Vero":
                        mail_sender.send_mail_pec(emails_info[0], code_group[1])
                    else:
                        raise ValueError("Can't read mail type value!")
                    # Move pdf file to "sent" folder
                    utils.move_pdf_to_sent_folder(code_group[1])
                except ValueError:
                    logging.warning("Error decoding "+utils.read_config_value('PATH', 'clients_filename') + " for client " +
                                  code)
            except ValueError:
                logging.warning("Can't find email address for client: " + code)
    input("Prese <Enter> to exit.")
