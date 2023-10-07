#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 23:01:16 2023

@author: jules
"""
import os
import shutil
import logging

class InitManager:
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    def _copy_file(self, source_path, destination_path):
        if not os.path.exists(destination_path):
            shutil.copy2(source_path, destination_path)
            os.chmod(destination_path, 0o666)  # rw-rw-rw- (read, write permissions for everyone)
            logging.info(f'Create {destination_path}')

    def _create_directory(self, destination_path):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
            logging.info(f'Create {destination_path}')

    def copy_configs(self):
        if not os.path.exists(self.source_folder):
            logging.warning(f'Source folder {self.source_folder} does not exist.')
            return

        for root, dirs, files in os.walk(self.source_folder):
            for dir_name in dirs:
                source_path = os.path.join(root, dir_name)
                destination_path = os.path.join(self.destination_folder, os.path.relpath(source_path, self.source_folder))
                logging.info(f'{source_path} -> {destination_path}')
                self._create_directory(destination_path)

            for file_name in files:
                source_path = os.path.join(root, file_name)
                destination_path = os.path.join(self.destination_folder, os.path.relpath(source_path, self.source_folder))
                logging.info(f'{source_path} -> {destination_path}')
                self._copy_file(source_path, destination_path)


if __name__ == "__main__":
    source_folder = './_init'
    destination_folder = os.getenv('MOUNTPOINT', f'{os.getcwd()}/mnt/')

    init_manager = InitManager(source_folder, destination_folder)
    init_manager.copy_configs()
