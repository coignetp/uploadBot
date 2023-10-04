# Simple Python module to upload files to Google Drive
# Needs a file 'client_secrets.json' in the directory
# The file can be obtained from https://console.developers.google.com/
# under APIs&Auth/Credentials/Create Client ID for native application

import os
import logging
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class Drive:
    def __init__(self):
        # Initialize the logger
        self.logger = logging.getLogger(__name__)
        self.gauth = None
        self.drive = None
        self.initialize()

    def initialize(self):
        # Initialize GoogleAuth object and authenticate
        self.gauth = GoogleAuth()
        self.logger.debug("Authenticating with Google Drive...")

        # Try to load existing credentials or authenticate if not present
        if not self.gauth.LoadCredentialsFile("mycreds.txt"):
            self.logger.debug("No existing credentials found. Initiating authentication...")
            self.gauth.LocalWebserverAuth()  # Authenticate using the local webserver
            self.gauth.SaveCredentialsFile("mycreds.txt")
        else:
            self.logger.debug("Credentials loaded successfully.")

        # Create a GoogleDrive instance with authenticated GoogleAuth object
        self.drive = GoogleDrive(self.gauth)

    def find_folders(self, folder_name):
        # Search for folders matching the specified name
        query = f"title='{folder_name}' and mimeType contains 'application/vnd.google-apps.folder' and trashed=false"
        self.logger.debug(f"Searching for folders with query: {query}")
        file_list = self.drive.ListFile({"q": query}).GetList()
        return file_list

    def create_subfolder(self, folder, sub_folder_name):
        # Create a subfolder within the specified parent folder
        new_folder = self.drive.CreateFile({
            "title": sub_folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        })
        if folder is not None:
            new_folder["parents"] = [{"id": folder["id"]}]
        new_folder.Upload()
        self.logger.debug(f"Created subfolder: {sub_folder_name} under parent folder: {folder}")
        return new_folder

    def upload_files_to_folder(self, fnames, folder):
        # Upload files to the specified folder
        for fname in fnames:
            nfile = self.drive.CreateFile({
                "title": os.path.basename(fname),
                "parents": [{"id": folder["id"]}],
            })
            nfile.SetContentFile(fname)
            nfile.Upload()
            self.logger.debug(f"Uploaded file: {os.path.basename(fname)} to folder: {folder}")
