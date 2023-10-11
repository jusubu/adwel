#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:01:57 2023

@author: jules
"""

import platform
import subprocess
import logging
import time

class VPNManager:
    CONNECT_COMMANDS = {
        "Windows": ["rasdial", "{vpn_name}", "{vpn_username}", "{vpn_password}"],
#        "Linux": ["nmcli", "connection", "up", "id", "{vpn_name}"],
        "Linux": ["sudo", "pon", "{vpn_name}"],
        "Darwin": ["sudo", "networksetup", "-connectpppoeservice", "{vpn_name}"]
    }

    DISCONNECT_COMMANDS = {
        "Windows": ["rasphone", "-h", "{vpn_name}"],
#        "Linux": ["nmcli", "connection", "down", "id", "{vpn_name}"],
        "Linux": ["sudo", "poff", "{vpn_name}"],
        "Darwin": ["sudo", "networksetup", "-disconnectpppoeservice", "{vpn_name}"]
    }

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
        self.timeout_seconds = 20 # connection time out
        self.wait_seconds = 2 # wait time after vpn connect

        # Construct connect and disconnect commands based on the platform.
        self.connect_command = self._construct_command(self.CONNECT_COMMANDS)
        self.disconnect_command = self._construct_command(self.DISCONNECT_COMMANDS)
        logging.info(self.__class__.__name__)

    def _create_vpn_connection(self):
        """
        Disclaimer: 
        This function creates the VPN connection but the vpn-connection is not complete
        It connects to the server fine, but after that nothing....
        edit: Probably it needs a 'route' to the vpn-network

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

    def _construct_command(self, command_dict):
        """
        Construct the VPN connection command based on the operating system.

        Args:
            command_dict (dict): A dictionary of platform-specific command templates.

        Returns:
            list: A list representing the command to connect or disconnect from the VPN.
        """
        platform_name = platform.system()
        command_template = command_dict.get(platform_name)
        if command_template:
            return [part.format(
                vpn_name=self.vpn_name,
                vpn_username=self.vpn_username,
                vpn_password=self.vpn_password
            ) for part in command_template]
        else:
            logging.error("Unsupported operating system.")
            return []
        
    def _construct_connect_command(self):
        """
        Construct the VPN connection command based on the operating system.

        Returns:
            list: A list representing the command to connect or disconnect from the VPN.
        """
        return self._construct_command(self.CONNECT_COMMANDS)
    
    def _construct_disconnect_command(self):
        """
        Construct the VPN disconnection command based on the operating system.

        Returns:
            list: A list representing the command to disconnect from the VPN.
        """
        return self._construct_command(self.DISCONNECT_COMMANDS)


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
        
    def linux_vpn_connected(self):
        """
        Check if the VPN in linux is connected.

        Returns:
            bool: False if not connected, True otherwise.
        """
        try:
            result = subprocess.run(
                ["ip", "link", "show", "dev", "ppp0"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

            # If 'Device "ppp0" does not exist' is found in the error output, return False
            if "does not exist" in result.stderr:
                logging.info(f'No interface yet: {result.stderr}')
                return False

            # Check if the interface is up in the standard output
            if "UP" in result.stdout:
                logging.info(f'Interface is up: {result.stdout}')
                return True
            else:
                logging.info(f'Interface not up: {result.stdout}')
                return False
            
        except subprocess.CalledProcessError as e:
            return False
        
    def _is_already_connected(self):
        """
        Check if the VPN is already connected.

        Returns:
            bool: True if the VPN is already connected, False otherwise.
        """
        if platform.system() == "Windows":
            check_command = ["rasdial", self.vpn_name]
        elif platform.system() == "Linux":
            return self.linux_vpn_connected()
        # elif platform.system() == "Linux":
        #     check_command = ["nmcli", "-t", "-f", "GENERAL.STATE", "connection", "show", "--active", "id", self.vpn_name]
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
        First check if VPN already active.
        # If the VPN connection doesn't exist, it will be created first

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        if self._is_already_connected():
            # the connection made by the following function needs debugging
            # if not self._create_vpn_connection():
            logging.info(f'Already connected')
            return True

        if not self.connect_command:
            return False
            
        returncode = self._execute_command(self.connect_command)
        logging.info(f'returncode {returncode}')
        time.sleep(self.wait_seconds) # give vpn connection some time to get itself and it's route up
        return returncode == 0

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
    else:
        print(f'failed to connect to {vpn_connection.vpn_name}')
    sleep(5)
    if vpn_connection.disconnect():
        print('disconnected')