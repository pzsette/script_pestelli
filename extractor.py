import csv
import os
import path_utils
from collections import defaultdict
import logging


def scan_pdfs():
    path = path_utils.get_to_send_folder_path()
    files = os.listdir(path)
    return add_values_in_dict(files)


def find_emails(code):
    email_info = None
    with open(path_utils.get_clients_file()) as csvDataFile:
        csv_reader = csv.reader(csvDataFile)
        for row in csv_reader:
            split_row = row[0].split("#")
            if len(split_row) != 4:
                logging.error("Error format in customer line: "+row[0]+"\n")
            elif split_row[0] == code:
                email_info = split_row[2], split_row[3]
    if email_info is None:
        raise ValueError("Can't find mail address!\n")
    return email_info


def add_values_in_dict(files):
    pdf_for_key = defaultdict(list)
    for entry in files:
        if entry.__contains__('.pdf'):
            code = entry[0:6]
            if code.isdecimal():
                pdf_for_key[code].append(entry)
            else:
                logging.warning("Can't extract code from: "+entry+"\n")
    return pdf_for_key
