#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:58:00 2023

@author: jules
"""
import os
import logging

LOGFILE = 'scraper.log'

def setup_logging(basedir, log_file=LOGFILE):
    
    # # Create a logger and add a FileHandler with the regular format
    # # logger = logging.getLogger(__name__)
    # logging.setLevel(logging.INFO)

    # # Define the regular formatter
    # formatter = logging.Formatter(
    #     "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s"
    # )

    # file_handler = logging.FileHandler(log_file)
    # format1stline = logging.Formatter("%(asctime)s - %(message)s")
    # file_handler.setFormatter(format1stline)
    # logging.addHandler(file_handler)
    # # Log the first line with a custom format
    # logging.info("*** Program started ***")
    # # Log subsequent messages with the regular format
    # file_handler.setFormatter(formatter)
    # logging.info("2nd line")

    log_file = os.path.join(basedir, log_file)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s",
    )
    

if __name__ == "__main__":
    from pathlib import Path

    print(Path(__file__).name)

    setup_logging(os.getcwd())
    logging.info('test')