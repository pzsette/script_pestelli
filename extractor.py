import csv
import os
import utils
from collections import defaultdict
import logging


def scan_pdfs():
    path = utils.read_config_value('PATH', 'path_to_send')
    files = os.listdir(path)
    return add_values_in_dict(files)


def find_emails(code):
    email_info = None
    data_path = utils.read_config_value('PATH', 'data')
    with open(data_path + utils.read_config_value('PATH', 'clients_filename')) as csvDataFile:
        csv_reader = csv.reader(csvDataFile)
        for row in csv_reader:
            split_row = row[0].split("#")
            if split_row[0] == code:
                email_info = split_row[2], split_row[3]
    if email_info is None:
        raise ValueError("Can't find mail address!")
    return email_info


def add_values_in_dict(files):
    pdf_for_key = defaultdict(list)
    for entry in files:
        code = entry[0:6]
        if code.isdecimal():
            pdf_for_key[code].append(entry)
        else:
            logging.warning("Can't extract code from: "+entry)
    return pdf_for_key
