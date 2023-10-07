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
        sender_email = self.config.get("mail", "sender_email")
        recipient_email = self.config.get("mail", "recipient_email")
        subject = self.config.get("mail", "subject")
        message_body = self.config.get("mail", "message_body")

        # Create an email message object.
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message_body, "plain"))

        if attachments:
            # Attach files to the email message.
            self.attach_files(msg, attachments)

        smtp_server = self.config.get("smtp", "smtp_server")
        smtp_port = int(self.config.get("smtp", "smtp_port"))
        smtp_username = self.config.get("smtp", "smtp_username")
        smtp_password = self.config.get("smtp", "smtp_password")

        try:
            # Connect to the SMTP server and send the email.
            with smtplib.SMTP(smtp_server, smtp_port, timeout=self.timeout_seconds) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())

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
            canonical_path(config.get("folders","base_dir")),
            config.get("folders", "csv_result")
        ).split()
    email_manager.send_email(attachme)
