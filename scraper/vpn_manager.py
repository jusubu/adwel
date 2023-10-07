#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:01:57 2023

@author: jules
"""

import platform
import subprocess
import logging

class VPNManager:
    def __init__(self, config):
        """
        Initialize the VPNManager with configuration settings.

        Args:
            config (dict): A dictionary containing VPN configuration settings.

        Returns:
            None
        """
        self.config = config
        self.vpn_name = self.config.get("vpn", "vpn_name")
        self.vpn_username = self.config.get("vpn", "vpn_username")
        self.vpn_password = self.config.get("vpn", "vpn_password")
        self.timeout_seconds = 20

        # Construct connect and disconnect commands based on the platform.
        self.connect_command = self._construct_connect_command()
        self.disconnect_command = self._construct_disconnect_command()
        logging.info(self.__class__.__name__)

    def _create_vpn_connection(self):
        """
        Disclaimer: This function creates the VPN connection but the vpn-connection is bugged
        It connects to the server fine, but after that nothing....

        Create the PPTP VPN connection using NetworkManager on Linux or rasdial on Windows
        with MSCHAP and MSCHAPv2 authentication.

        Returns:
            bool: True if the creation was successful, False otherwise.
        """
        if platform.system() == "Linux":
            # Define the command as a list of arguments
            create_command = [
                'nmcli',
                'connection',
                'add',
                'con-name', f'{self.vpn_name}',
                'type', 'vpn',
                'vpn-type', 'pptp',
                'ifname', '*',
                'connection.autoconnect', 'off',
                # 'connection.permissions', f'user:{your_username}',
                'ipv4.dns-search', '',
                'ipv4.method', 'auto',
                'ipv4.never-default', 'true',
                'ipv6.dns-search', '',
                'ipv6.method', 'auto',
                'ipv6.never-default', 'true',
                '+vpn.data', 'gateway=82.139.77.43',
                '+vpn.data', 'lcp-echo-failure=5',
                '+vpn.data', 'lcp-echo-interval=30',
                '+vpn.data', 'password-flags=1',
                '+vpn.data', 'refuse-chap=yes',
                '+vpn.data', 'refuse-eap=yes',
                '+vpn.data', 'refuse-pap=yes',
                '+vpn.data', 'require-mppe=yes',
                '+vpn.data', f'user={self.vpn_username}',
                '+vpn.data', 'service-type=org.freedesktop.NetworkManager.pptp',
                '+vpn.secret', f'password={self.vpn_password}'
            ]

            returncode = self._execute_command(create_command)

            logging.info(f"Create VPN Command: {' '.join(create_command)}")
            logging.info(f'returncode {returncode}')

            return returncode == 0

        elif platform.system() == "Windows":
            create_command = [
                "rasdial",
                self.vpn_name,
                self.vpn_username,
                self.vpn_password,
            ]
            returncode = self._execute_command(create_command)
            logging.info(f"Create VPN Command: {' '.join(create_command)}")
            logging.info(f'returncode {returncode}')
            return  returncode == 0
        else:
            logging.error("Unsupported operating system.")
            return False

    def _construct_connect_command(self):
        """
        Construct the VPN connection command based on the operating system.

        Returns:
            list: A list representing the command to connect to the VPN.
        """
        if platform.system() == "Windows":
            return ["rasdial", self.vpn_name, self.vpn_username, self.vpn_password]
        elif platform.system() == "Linux":
            return ["nmcli", "connection", "up", "id", self.vpn_name]
        elif platform.system() == "Darwin":  # macOS (not tested)
            return ["sudo", "networksetup", "-connectpppoeservice", self.vpn_name]
        else:
            logging.error("Unsupported operating system.")
            return []

    def _construct_disconnect_command(self):
        """
        Construct the VPN disconnection command based on the operating system.

        Returns:
            list: A list representing the command to disconnect from the VPN.
        """
        if platform.system() == "Windows":
            return ["rasphone", "-h", self.vpn_name]
        elif platform.system() == "Linux":
            return ["nmcli", "connection", "down", "id", self.vpn_name]
        elif platform.system() == "Darwin":  # macOS (not tested)
            return ["sudo", "networksetup", "-disconnectpppoeservice", self.vpn_name]
        else:
            logging.error("Unsupported operating system.")
            return []

    def _execute_command(self, command):
        """
        Execute a command using subprocess and handle errors.

        Args:
            command (list): A list representing the command to be executed.

        Returns:
            int: Return code of the executed command.
        """
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout_seconds, check=False
            )
            
            return result.returncode
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed with error: {e}")
            return -1
        except subprocess.TimeoutExpired as e:
            logging.error(f"Command timed out: {e}")
            return -1

    def _is_already_connected(self):
        """
        Check if the VPN is already connected.

        Returns:
            bool: True if the VPN is already connected, False otherwise.
        """
        if platform.system() == "Windows":
            check_command = ["rasdial", self.vpn_name]
        elif platform.system() == "Linux":
            check_command = ["nmcli", "-t", "-f", "GENERAL.STATE", "connection", "show", "--active", "id", self.vpn_name]
        elif platform.system() == "Darwin":
            check_command = ["sudo", "networksetup", "-getinfo", self.vpn_name]
        else:
            logging.error("Unsupported operating system.")
            return False

        returncode = self._execute_command(check_command)

        if returncode == 0:
            logging.info(f"Already connected to {self.vpn_name}")
        else:
            logging.info(f'returncode {returncode}')

        return returncode == 0

    def connect(self):
        """
        Connect to the VPN using the configured connection command.
        If the VPN connection doesn't exist, it will be created first.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        if not self.connect_command:
            return False

        if not self._is_already_connected():
            # the connection made by the following function needs debugging
            # if not self._create_vpn_connection():
            return False
            
        returncode = self._execute_command(self.connect_command)
        logging.info(f'returncode {returncode}')
        return  returncode == 0

    def disconnect(self):
        """
        Disconnect from the VPN using the configured disconnection command.

        Returns:
            bool: True if the disconnection was successful, False otherwise.
        """
        if not self.disconnect_command:
            return False
        
        returncode = self._execute_command(self.disconnect_command)
        logging.info(f'returncode {returncode}')
        return  returncode == 0


if __name__ == "__main__":
    from time import sleep
    # add workspace-path to the %PATH% env
    import sys
    sys.path.append(".")

    # local modules
    from core.configuration_manager import ConfigurationManager
    config = ConfigurationManager()

    vpn_connection = VPNManager(config)
    if vpn_connection.connect():
        print(f'connected to {vpn_connection.vpn_name}')
    sleep(5)
    if vpn_connection.disconnect():
        print('disconnected')