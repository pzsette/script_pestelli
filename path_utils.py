import os
import utils


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
