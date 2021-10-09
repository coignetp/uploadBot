# Simple Python module to upload files to Google Drive
# Needs a file 'client_secrets.json' in the directory
# The file can be obtained from https://console.developers.google.com/
# under APIs&Auth/Credentials/Create Client ID for native application

import logging
import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class Drive(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.login()

    def login(self):
        self.gauth = GoogleAuth()

        self.gauth.LoadCredentialsFile("mycreds.txt")
        self.logger.debug("Loading credentials")

        if self.gauth.credentials is None:
            self.logger.debug("First authentication")
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.logger.debug("Token has expired, refreshing")
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            self.logger.debug("Connected")
            # Initialize the saved creds
            self.gauth.Authorize()
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile("mycreds.txt")

        # Create GoogleDrive instance with authenticated GoogleAuth instance
        self.drive = GoogleDrive(self.gauth)

    def find_folders(self, folder_name):
        file_list = self.drive.ListFile(
            {
                "q": "title='{}' and mimeType contains 'application/vnd.google-apps.folder' and trashed=false".format(
                    folder_name
                )
            }
        ).GetList()
        return file_list

    def create_subfolder(self, folder, sub_folder_name):
        new_folder = self.drive.CreateFile(
            {
                "title": "{}".format(sub_folder_name),
                "mimeType": "application/vnd.google-apps.folder",
            }
        )
        if folder is not None:
            new_folder["parents"] = [{u"id": folder["id"]}]
        new_folder.Upload()
        self.logger.debug("Folder created {}/{}".format(folder, sub_folder_name))
        return new_folder

    def upload_files_to_folder(self, fnames, folder):
        for fname in fnames:
            nfile = self.drive.CreateFile(
                {"title": os.path.basename(fname), "parents": [{u"id": folder["id"]}]}
            )
            nfile.SetContentFile(fname)
            nfile.Upload()
