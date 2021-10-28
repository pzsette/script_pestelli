import sys
import extractor
from mail_sender import *
import logging


def set_logging_conf():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt='%d-%b-%y %H:%M:%S',
        handlers=[
            logging.FileHandler("output.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.getLogger().setLevel(logging.INFO)


if __name__ == '__main__':

    path_utils.check_if_all_paths_exist()

    set_logging_conf()

    mail_sender = MailSender()

    # ask user month and year
    date = utils.get_date_info()
    if date is None:
        logging.error("Error getting date info")
        utils.end_execution()

    # assign to mail_sender
    mail_sender.set_month(date[0])
    mail_sender.set_year(date[1])

    # Group pdf files by their code "007: {1.pdf, 2.pdf, 3.pdf}, 002: {4.pdf},..."
    pdf_files_by_code = extractor.scan_pdfs()
    # Perform this routine for every code
    for code_group in pdf_files_by_code.items():
        code = code_group[0]
        pdf_list = code_group[1]
        try:
            # get customer associated to this code and mail type
            customer = extractor.find_customer_by_code(code)
            # sent pdf_list to customer
            mail_sender.sent_pdf_list_to_customer(customer, pdf_list)
        except ValueError:
            logging.warning("Can't find email address for client: " + code+"\n")
        except SyntaxError:
            logging.warning("Error in mail type value for client: " + code+"\n")
    utils.end_execution()
