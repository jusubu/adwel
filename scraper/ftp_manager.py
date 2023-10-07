#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:03:02 2023

@author: jules
"""

import os
import logging
from ftplib import FTP

# add workspace-path to the %PATH% env
import sys
sys.path.append(".")

# local modules
from core.utils import canonical_path

# Constants
FTP_SUCCESS_CODE = "226"

class FTPManager:
    def __init__(self, config):
        """
        Initialize the FTPManager with configuration settings and create an FTP connection.

        Args:
            config (dict): A dictionary containing FTP configuration settings.

        Returns:
            None
        """
        self.config = config
        self.ftp = FTP()
        self.remote_directory = self.config.get("ftp", "remote_directory")
        self.timeout_seconds = 20
        logging.info(self.__class__.__name__)

    def connect(self):
        """
        Connect to the FTP server using the provided configuration.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            ftp_server = self.config.get("ftp", "ftp_server")
            ftp_port = int(self.config.get("ftp", "ftp_port"))
            ftp_user = self.config.get("ftp", "ftp_user")
            ftp_password = self.config.get("ftp", "ftp_password")

            self.ftp.connect(ftp_server, ftp_port, timeout=self.timeout_seconds)
            self.ftp.login(ftp_user, ftp_password)

            logging.info(f"Connected to FTP server: {ftp_server}:{ftp_port}")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to FTP server: {e}")
            return False

    def list_remote_files(self):
        """
        List files in the remote directory of the FTP server.

        Returns:
            list: A list of file names in the remote directory.
        """
        try:
            file_list = self.ftp.nlst(self.remote_directory)
            return file_list
        except Exception as e:
            logging.error(f"Error listing files on the FTP server: {e}")
            return []

    def download_files(self, download_directory):
        """
        Download CSV files from the FTP server to the local directory.

        Args:
            download_directory (str): The local directory where files will be downloaded.

        Returns:
            list: A list of downloaded CSV file paths.
        """
        # download_directory = canonical_path(download_directory)

        try:
            if not os.path.exists(download_directory):
                os.makedirs(download_directory, exist_ok=True)

            csv_list = []
            remote_files = self.list_remote_files()

            for filename in remote_files:
                if filename.lower().endswith(".csv"):
                    remote_path = os.path.join(self.remote_directory, filename)
                    local_path = os.path.join(download_directory, filename)

                    with open(local_path, "wb") as local_file:
                        ftp_response = self.ftp.retrbinary(f"RETR {remote_path}", local_file.write)

                    # Check if the local file exists before deleting the remote file
                    # if os.path.exists(local_path):
                    if FTP_SUCCESS_CODE in ftp_response:
                        self.ftp.delete(remote_path)  # Remove the file from the FTP server
                        logging.info(f"Downloaded and deleted remote file: {filename} ({ftp_response})")
                        csv_list.append(local_path)
                    else:
                        logging.error(f"Downloaded file does not exist: {local_path}")

            return csv_list
        except Exception as e:
            logging.error(f"Error downloading files: {e}")
            return []

    def ftp_has_files(self):
        return len(self.ftp.nlst(self.remote_directory)) > 2  # Ignore . and ..


if __name__ == "__main__":
    # local modules
    from core.configuration_manager import ConfigurationManager
    from vpn_manager import VPNManager
    
    config = ConfigurationManager()
    vpn_manager = VPNManager(config)
    vpn_manager.connect()

    ftp_manager = FTPManager(config)

    if ftp_manager.connect():
        print(ftp_manager.list_remote_files())
        
    vpn_manager.disconnect()
