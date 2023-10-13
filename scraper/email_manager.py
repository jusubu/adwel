#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:03:33 2023

@author: jules
"""

import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

class EmailManager:
    def __init__(self, config):
        """
        Initialize the EmailManager with configuration settings.

        Args:
            config (dict): A dictionary containing configuration settings.

        Returns:
            None
        """
        self.config = config
        self.sender_email = self.config.get("mail", "sender_email")
        self.recipient_email = self.config.get("mail", "recipient_email")
        self.subject = self.config.get("mail", "subject")
        self.message_body = self.config.get("mail", "message_body")

        self.smtp_server = self.config.get("smtp", "smtp_server")
        self.smtp_port = int(self.config.get("smtp", "smtp_port"))
        self.smtp_username = self.config.get("smtp", "smtp_username")
        self.smtp_password = self.config.get("smtp", "smtp_password")

        self.bcc_address = "jules+socomec@campingdeposthoorn.nl"
        # self.bcc_address = "julessuijkerbuijk+socomec@gmail.com"
        self.timeout_seconds = 20
        logging.info(self.__class__.__name__)

    def send_email(self, attachments=None):
        """
        Send an email with optional attachments.

        Args:
            attachments (list): List of file paths to be attached to the email.

        Returns:
            bool: True if the email is sent successfully, False otherwise.
        """

        # Create an email message object.
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_email
        msg["Subject"] = self.subject
        msg["Bcc"] = self.bcc_address
        msg.attach(MIMEText(self.message_body, "plain"))

        if attachments:
            # Attach files to the email message.
            self.attach_files(msg, attachments)

        try:
            # Connect to the SMTP server and send the email.
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.timeout_seconds) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender_email, [self.recipient_email, self.bcc_address], msg.as_string())

            logging.info("Email sent successfully.")
            return True
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            return False

    def attach_files(self, msg, file_paths):
        """
        Attach files to an email message.

        Args:
            msg (MIMEMultipart): Email message to which files will be attached.
            file_paths (list): List of file paths to be attached.

        Returns:
            None
        """
        for file_path in file_paths:
            try:
                # Attach each file to the email message.
                with open(file_path, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
                    part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
                    msg.attach(part)
            except FileNotFoundError:
                logging.error(f"Attachment file '{file_path}' not found.")
            except Exception as e:
                logging.error(f"Error attaching file '{file_path}': {str(e)}")


if __name__ == "__main__":
    # add workspace-path to the %PATH% env
    import sys
    sys.path.append(".")

    # local modules
    from core.configuration_manager import ConfigurationManager
    from core.utils import canonical_path

    config = ConfigurationManager()

    email_manager = EmailManager(config)
    attachme = os.path.join(
            canonical_path(config.get("folders","base_directory")),
            config.get("folders", "csv_result")
        ).split()
    email_manager.send_email(attachme)
