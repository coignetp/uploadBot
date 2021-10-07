# Simple Python module to upload files to Google Drive
# Needs a file 'client_secrets.json' in the directory
# The file can be obtained from https://console.developers.google.com/
# under APIs&Auth/Credentials/Create Client ID for native application


import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def login():
    global gauth, drive
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("mycreds.txt")
    print("Loading credentials")

    if gauth.credentials is None:
        print("First")
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        print("Second")
        # Refresh them if expired
        gauth.Refresh()
    else:
        print("Third")
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    # Create GoogleDrive instance with authenticated GoogleAuth instance
    drive = GoogleDrive(gauth)


def root_files():
    file_list = drive.ListFile(
        {'q': "'root' in parents and trashed=false"}).GetList()
    return file_list


def find_folders(fldname):
    file_list = drive.ListFile({
        'q': "title='{}' and mimeType contains 'application/vnd.google-apps.folder' and trashed=false".format(fldname)
    }).GetList()
    return file_list


def create_subfolder(folder, sfldname):
    new_folder = drive.CreateFile({'title': '{}'.format(sfldname),
                                   'mimeType': 'application/vnd.google-apps.folder'})
    if folder is not None:
        new_folder['parents'] = [{u'id': folder['id']}]
    new_folder.Upload()
    return new_folder


def list_files_with_ext(ext, dir='./'):
    return sorted(filter(lambda f: f[-len(ext):] == ext, os.listdir(dir)))


def upload_files_to_folder(fnames, folder):
    for fname in fnames:
        nfile = drive.CreateFile({'title': os.path.basename(fname),
                                  'parents': [{u'id': folder['id']}]})
        nfile.SetContentFile(fname)
        nfile.Upload()
