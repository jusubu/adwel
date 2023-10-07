
"""
Created on Tue Sep 26 16:59:56 2023

@author: jules
"""

import os
import logging
from pathlib import Path
import time

# add workspace-path to the %PATH% env
# import sys
# sys.path.append(".") # local hack for sibling import
# sys.path.append("..") # docker hack for sibling import

# local modules
from core.logging_manager import setup_logging
from core.configuration_manager import ConfigurationManager
from core.init_manager import InitManager
from core.utils import canonical_path

from scraper.vpn_manager import VPNManager
from scraper.ftp_manager import FTPManager
from scraper.email_manager import EmailManager
from scraper.data_manager import DataManager

INI_FILE = "socomec.ini"
INIT_FOLDER = "init/" # contains folder structure, empty database and ini-file for setup
BASE_FOLDER = "mnt/" # the root for all data, logs and configs

def main():
    # setup the path to the working directory for local and docker use
    local_base_dir = Path(os.getcwd()).resolve().parents[0] # parent dir of current project path
    local_base_dir = canonical_path(os.path.join(local_base_dir, BASE_FOLDER)) # the root for all data, logs and configs
    base_dir = canonical_path(os.getenv('MOUNT_POINT', local_base_dir)) # for use in docker
    init_dir = canonical_path(os.path.join(os.getcwd(),INIT_FOLDER)) # template for the folder structure and empty database
    # print(f'basedir = {base_dir}')
    # print(f'init_dir = {init_dir}')

    # activate logging
    setup_logging(base_dir)
    logging.info("*** *** *** Program Start *** *** ***")

    # initialize folders, config and database
    init_manager = InitManager(init_dir, base_dir)
    init_manager.copy_configs()

    # read config from ini-file
    ini_file = canonical_path(os.path.join(base_dir,INI_FILE))
    # print(f'ini_file = {ini_file}')
    config = ConfigurationManager(ini_file)
    # print(config.get_sections())

    data_dir = canonical_path(os.path.join(base_dir, config.get("folders","download_folder")))
    backup_dir = canonical_path(os.path.join(base_dir, config.get("folders","backup_folder")))
    
    try:
        data_manager = DataManager(config)

        reading_list = []

        # empty (process+archive) the download folder before downloading a new batch
        if data_manager.local_has_csv(data_dir):
            reading_list = data_manager.read_csv_files(data_dir, base_dir)
            data_manager.process_and_save_to_db(reading_list, base_dir)
            data_manager.archive_files(data_dir, backup_dir)
            reading_list = []

        vpn_manager = VPNManager(config)
        if vpn_manager.connect():
            ftp_manager = FTPManager(config)
            if ftp_manager.connect():
                if ftp_manager.download_files(data_dir):
                    email_manager = EmailManager(config)
                    reading_list = data_manager.read_csv_files(data_dir, base_dir)
                    data_manager.process_and_save_to_db(reading_list, base_dir)
                    data_manager.archive_files(data_dir, backup_dir)
                    attachme = os.path.join(
                        base_dir,
                        config.get("folders", "csv_result")
                    ).split()
                    email_manager.send_email(attachme)
                else:
                    logging.warning("No CSV files on server.")
        else:
            logging.error(f'Cannot connect to vpn ({vpn_manager.vpn_name})')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        vpn_manager.disconnect()
        logging.info("** *** *** *** *** *** *** *** *** **")


if __name__ == "__main__":
    main()
