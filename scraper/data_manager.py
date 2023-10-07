#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:04:00 2023

@author: jules
"""

import os
import glob
import pandas as pd
import sqlite3
import logging
from datetime import datetime
from py7zr import SevenZipFile

# add workspace-path to the %PATH% env
import sys
sys.path.append(".")

# local modules
from core.configuration_manager import ConfigurationManager
from core.utils import canonical_path


class DataManager:
    def __init__(self, config):
        """
        Initialize the DataManager with configuration settings.

        Args:
            config (dict): A dictionary containing configuration settings.

        Returns:
            None
        """
        self.config = config
        self.csv_result = self.config.get("folders", "csv_result")
        self.db_name = self.config.get("folders", "db_name")
        self.timeout_seconds = 20
        logging.info(self.__class__.__name__)


    def local_has_csv(self, datadir):
        """
        Checks for csv files in a directory.

        Args:
            datadir (str): The directory to be checked.

        Returns:
            Bool: True if there are csv files. False otherwise.
        """

        # datadir = canonical_path(datadir)
        return any(
            filename.lower().endswith(".csv")
            for filename in os.listdir(datadir)
        )


    def read_csv_files(self, datadir, resultdir):
        """
        Read CSV files from a directory, process the data, and save results to a csv-file.

        Args:
            datadir (str): The directory containing CSV files to be processed.
            resultdir (str): The directory where result file will be saved.

        Returns:
            list: A list of dictionaries representing processed data.
        """
        # Get the CSV result filename from the configuration

        # datadir = canonical_path(datadir)
        # resultdir = canonical_path(resultdir)
        
        result_list = []

        try:
            # Iterate through CSV files in the specified directory
            for path in glob.iglob(os.path.join(datadir, "?*@*.csv")): # skip files without '@' in filename
                df = pd.read_csv(path, header=None, usecols=[0, 1, 4])

                if len(df) > 1:
                    metername = df.iloc[1, 0]
                    meterdate = df.iloc[1, 2]
                else:
                    metername, meterdate = "", ""

                if len(df) > 8:
                    meterdate = df.iloc[8, 0]
                    metervalue = df.iloc[8, 1]
                else:
                    metervalue = 0

                addressname = str(metername).split("_")[0]

                result_list.append(
                    {
                        "MeterName": metername,
                        "AddressName": addressname,
                        "MeterValue": metervalue,
                        "MeterDate": meterdate,
                    }
                )

            # Sort the result list by MeterName
            result_list = sorted(result_list, key=lambda k: k["MeterName"])

            # Create a DataFrame from the result list
            df_result = pd.DataFrame(
                result_list, columns=["MeterName", "AddressName", "MeterValue", "MeterDate"]
            )

            # Save the DataFrame as a CSV file
            df_result.to_csv(os.path.join(resultdir, self.csv_result), index=False)
            logging.info("CSV files read successfully.")

            return result_list
        except Exception as e:
            # Handle exceptions and log errors
            logging.error(f"An error occurred while reading CSV files: {e}")
            raise

    def process_and_save_to_db(self, result_list, basedir):
        """
        Process data and save it to a SQLite database.

        Args:
            result_list (list): A list of dictionaries representing processed data.
            basedir (str): The base directory where the database file will be located.

        Returns:
            None
        """

        db_path = canonical_path(os.path.join(basedir, self.db_name))

        try:
            with sqlite3.connect(db_path, timeout=self.timeout_seconds) as conn:
                cursor = conn.cursor()
                data_to_insert = []

                # Iterate through the result list and prepare data for insertion
                for reading in result_list:
                    MeterName = reading["MeterName"]
                    ReadingValue = reading["MeterValue"]
                    ReadingDate = reading["MeterDate"]
                    AddressText = reading["AddressName"]

                    # Step 1: Insert AddressText into the Addresses table (if it doesn't exist)
                    cursor.execute(
                        "INSERT OR IGNORE INTO Addresses (AddressText) VALUES (?)",
                        (AddressText,),
                    )

                    # Step 2: Insert MeterName into the Meters table (if it doesn't exist)
                    cursor.execute(
                        "INSERT OR IGNORE INTO Meters (MeterName, AddressID) SELECT ?, AddressID FROM Addresses WHERE AddressText = ?",
                        (MeterName, AddressText),
                    )

                    # Step 3: Prepare data for batch insertion into the Readings table
                    cursor.execute(
                        "SELECT Meters.MeterID FROM Meters WHERE Meters.MeterName = ?",
                        (MeterName,),
                    )
                    meter_id = cursor.fetchone()[0]
                    data_to_insert.append((meter_id, ReadingValue, ReadingDate))

                # Step 4: Batch insertion into the Readings table
                cursor.executemany(
                    "INSERT OR IGNORE INTO Readings (MeterID, ReadingValue, ReadingDate) VALUES (?, ?, ?)",
                    data_to_insert,
                )

            logging.info(f"{len(result_list)} readings inserted successfully.")
        except sqlite3.Error as e:
            # Handle database errors and log errors
            logging.error(f"An error occurred while saving data to the database: {e}")
            raise
        except IOError as e:
            # Handle IO errors and log errors
            logging.error(f"IO Error: {e}")
            raise

    def archive_files(self, datadir, backupdir):
        """
        Archive files and remove original files.

        Args:
            datadir (str): The directory containing files to be archived.
            backupdir (str): The directory where backup archives will be stored.

        Returns:
            str: The path to the created backup archive.
        """
        # datadir = canonical_path(datadir)
        # backupdir = canonical_path(backupdir)

        try:
            if not os.path.exists(backupdir):
                os.makedirs(backupdir)

            current_time = datetime.now().strftime("%Y%m%d@%H%M%S")
            backup_archive_path = os.path.join(backupdir, f'{current_time}.7z')

            with SevenZipFile(backup_archive_path, 'w') as archive:
                for root, _, files in os.walk(datadir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive.write(file_path, os.path.relpath(file_path, datadir))

            for root, _, files in os.walk(datadir):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

            logging.info("Files archived and originals removed successfully.")
            return backup_archive_path
        except Exception as e:
            # Handle exceptions during archiving and log errors
            logging.error(f"Archive Error: {e}")
            raise


if __name__ == "__main__":
    from pathlib import Path

    print(Path(__file__).name)

    config = ConfigurationManager("socomec.ini")
