import os
import shutil
from pathlib import Path
import configparser


# move pdf files in the list to "sent" folder
def move_pdf_to_sent_folder(pdf_list):
    for pdf in pdf_list:
        shutil.copy(read_config_value('PATH', 'path_to_send') + pdf, read_config_value('PATH', 'path_sent'))
        os.remove(os.path.join(read_config_value('PATH', 'path_to_send'), pdf))


def read_subject_content():
    return Path(read_config_value('PATH', 'data') + read_config_value('PATH', 'subject_filename')).read_text()


def read_mail_content():
    return Path(read_config_value('PATH', 'data') + read_config_value('PATH', 'email_script_filename')).read_text()


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
