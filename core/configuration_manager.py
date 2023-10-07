#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:01:16 2023

@author: jules
"""

import configparser
import logging
from pathlib import Path

CONFIGFILE = 'socomec.ini'

"""
Singleton class for global configuration

Methods:
    get(key): get value for [key].
    get_sections(): Returns all section names.
    get_options(section): Return options for [section].
    read_file(filename): Parse and read content of [filename].

"""
class ConfigurationManager:
    _instances = {}

    def __new__(cls, config_file=CONFIGFILE):
        if config_file not in cls._instances:
            cls._instances[config_file] = super(ConfigurationManager, cls).__new__(cls)
            cls._instances[config_file]._config = configparser.ConfigParser()

            try:
                cls._instances[config_file]._config.read(config_file)
            except FileNotFoundError:
                logging.error(f"Configuration file '{config_file}' not found.")
                raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
            except Exception as e:
                logging.error(f"Error reading configuration file: {str(e)}")
                raise Exception(f"Error reading configuration file: {str(e)}")

        return cls._instances[config_file]

    def get(self, section, key):
        try:
            value = self._config.get(section, key)
            logging.info(f"Retrieved config value: Section='{section}', Key='{key}'")
            return value
        except configparser.NoOptionError:
            logging.error(f"Key '{key}' not found in section '{section}'")
            raise KeyError(f"Key '{key}' not found in section '{section}'")

    def get_sections(self):
        sections = self._config.sections()
        logging.info(f"Retrieved configuration sections: {sections}")
        return sections

    def get_options(self, section):
        options = self._config.options(section)
        logging.info(f"Retrieved options in section '{section}': {options}")
        return options

    def read_file(self, new_file):
        try:
            self._config.read(new_file)
            logging.info(f"Read configuration from file '{new_file}'")
        except FileNotFoundError:
            logging.error(f"Configuration file '{new_file}' not found.")
            raise FileNotFoundError(f"Configuration file '{new_file}' not found.")
        except Exception as e:
            logging.error(f"Error reading configuration file: {str(e)}")
            raise Exception(f"Error reading configuration file: {str(e)}")

if __name__ == "__main__":
    print(Path(__file__).name)

    custom_config_manager = ConfigurationManager()
    print(custom_config_manager.get_sections())

