import sys
import time
import telepot
from telepot.loop import MessageLoop
import datetime
import os
import json

import google_drive_util

# For french version. Can be changed.
monthNames = ["01 -Janvier", "02 - Fevrier", "03 - Mars", "04 - Avril", "05 - Mai", "06 - Juin",
              "07 - Juillet", "08 - Aout", "09 - Septembre", "10 - Octobre", "11 - Novembre", "12 - Decembre", "Inconnu"]
MainFolder = []


def getFolder(yearfold, monthfold, dayfold):
    foldersY = google_drive_util.find_folders(yearfold)

    if len(foldersY) == 0:
        foldersY.append(
            google_drive_util.create_subfolder(MainFolder, yearfold))

    foldersM = google_drive_util.find_folders(monthfold)

    if len(foldersM) == 0 or foldersM[-1].get('parents')[0].get('id') != foldersY[-1].get('id'):
        foldersM.append(google_drive_util.create_subfolder(
            foldersY[-1], monthfold))

    return foldersM[-1]


def uploadToDrive(fname, yearfold, monthfold, dayfold):
    folder = getFolder(yearfold, monthfold, dayfold)
    google_drive_util.upload_files_to_folder([fname], folder)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    now = datetime.datetime.now()
    if content_type == 'photo' or content_type == 'video':

        print(msg[content_type])
        fl = bot.getFile(msg[content_type][-1]['file_id'])

        filename = 'img_' + str(now.hour) + '-' + str(now.minute) + '-' + str(
            now.second) + '-' + str(now.microsecond) + '.' + fl['file_path'].split('.')[-1]

        bot.download_file(msg[content_type][-1]['file_id'], filename)

        uploadToDrive(filename, 'annee_' + str(now.year),
                      monthNames[now.month - 1], 'jour_' + str(now.day))

        os.remove(filename)


if __name__ == '__main__':
    configFilename = 'config.conf'

    with open(configFilename) as jsonFile:
        # Loads the configuration for the bot to work
        config = json.load(jsonFile)

        TOKEN = config["tg_token"]
        FOLDER = config["ggd_folder"]

        jsonFile.close()

        google_drive_util.login()
        MainFolder = google_drive_util.find_folders(FOLDER)[-1]

        # The bot is ready to start
        bot = telepot.Bot(TOKEN)
        MessageLoop(bot, handle).run_as_thread()
        print('Listening ...')

        while 1:
            time.sleep(10)
