import configparser
import os
import utils
import logging


def get_to_send_folder_path():
    return os.path.join(utils.read_config_value('PATH', 'file_folder'),
                        utils.read_config_value('PATH', 'to_send_folder'))


def get_sent_folder_path():
    return os.path.join(utils.read_config_value('PATH', 'file_folder'),
                        utils.read_config_value('PATH', 'sent_folder'))


def get_data_path():
    return os.path.join(utils.read_config_value('PATH', 'file_folder'),
                        utils.read_config_value('PATH', 'data_folder'))


def get_clients_file():
    return os.path.join(get_data_path(), utils.read_config_value('PATH', 'clients_filename'))


def get_email_script():
    return os.path.join(get_data_path(), utils.read_config_value('PATH', 'email_script_filename'))


def get_email_subject():
    return os.path.join(get_data_path(), utils.read_config_value('PATH', 'subject_filename'))


def check_if_all_paths_exist():
    if not os.path.isdir(get_to_send_folder_path()):
        logging.error("Can't find to send folder")
        utils.end_execution()
    if not os.path.isdir(get_sent_folder_path()):
        logging.error("Can't find sent folder")
        utils.end_execution()
    if not os.path.isdir(get_data_path()):
        logging.error("Can't find data folder")
        utils.end_execution()
    if not os.path.isfile(get_clients_file()):
        logging.error("Can't find customers file")
        utils.end_execution()
    if not os.path.isfile(get_email_script()):
        logging.error("Can't find email script")
        utils.end_execution()
    if not os.path.isfile(get_email_subject()):
        logging.error("Can't find subject file")
        utils.end_execution()
