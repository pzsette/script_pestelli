import os
import shutil
from pathlib import Path
import configparser
import path_utils
import logging


# move pdf files in the list to "sent" folder
def move_pdf_to_sent_folder(pdf_list):
    for pdf in pdf_list:
        filename, extension = os.path.splitext(pdf)
        if not os.path.exists(os.path.join(path_utils.get_sent_folder_path(), pdf)):
            shutil.copy(os.path.join(path_utils.get_to_send_folder_path(), pdf),
                        os.path.join(path_utils.get_sent_folder_path(), pdf))
            os.remove(os.path.join(path_utils.get_to_send_folder_path(), pdf))
        else:  # file already exists
            ii = 1
            while True:
                new_name = filename + "_" + str(ii) + extension
                if not os.path.exists(os.path.join(path_utils.get_sent_folder_path(), new_name)):
                    shutil.copy(os.path.join(path_utils.get_to_send_folder_path(), pdf),
                                os.path.join(path_utils.get_sent_folder_path(), new_name))
                    logging.info("copied " + pdf + " as " + new_name + " in destination folder\n")
                    os.remove(os.path.join(path_utils.get_to_send_folder_path(), pdf))
                    break
                ii += 1


def read_subject_content():
    return Path(path_utils.get_email_subject()).read_text()


def read_mail_content():
    return Path(path_utils.get_email_script()).read_text()


def read_config_value(section, value):
    config = configparser.ConfigParser()
    config.read("config_email.ini")
    return config[section][value]


def get_date_info():
    months = {'1': 'GENNAIO',
              '2': 'FEBBRAIO',
              '3': 'MARZO',
              '4': 'APRILE',
              '5': 'MAGGIO',
              '6': 'GIUGNO',
              '7': 'LUGLIO',
              '8': 'AGOSTO',
              '9': 'SETTEMBRE',
              '10': 'OTTOBRE',
              '11': 'NOVEMBRE',
              '12': 'DICEMBRE'}
    choice_month = input("Inserire mese (numero): ")
    if choice_month in months:
        month = months[choice_month]
    else:
        print("Errore inserimento mese (1->gennaio, 2-> febbraio, ...)")
        return None
    year = (input("Inserire anno: "))
    if not (year.isnumeric()):
        print("Errore inserimento anno")
        return None
    print('selezionato ' + month + ' ' + year)
    return [month, year]


def end_execution():
    log_end_execution()
    input("Press <Enter> to exit.")
    quit()


def log_end_execution():
    logging.info('--------------------------END EXECUTION--------------------------\n')
