import time
import telegram
import datetime
import os
import json

import google_drive_util

# For french version. Can be changed.
monthNames = ["01 -Janvier", "02 - Fevrier", "03 - Mars", "04 - Avril", "05 - Mai", "06 - Juin",
              "07 - Juillet", "08 - Aout", "09 - Septembre", "10 - Octobre", "11 - Novembre", "12 - Decembre", "Inconnu"]
MainFolder = []


def getFolder(yearfold, monthfold):
    foldersY = google_drive_util.find_folders(yearfold)

    if len(foldersY) == 0:
        foldersY.append(
            google_drive_util.create_subfolder(MainFolder, yearfold))

    foldersM = google_drive_util.find_folders(monthfold)

    if len(foldersM) == 0 or foldersM[-1].get('parents')[0].get('id') != foldersY[-1].get('id'):
        foldersM.append(google_drive_util.create_subfolder(
            foldersY[-1], monthfold))

    return foldersM[-1]


def uploadToDrive(fname, yearfold, monthfold):
    folder = getFolder(yearfold, monthfold)
    google_drive_util.upload_files_to_folder([fname], folder)


def handle(bot, msg):
    # content_type, chat_type, chat_id = telepot.glance(msg)

    file = None

    try:
        # Try photo first
        file = bot.getFile(msg.photo[0].file_id)
        print('Found a photo')
    except Exception:
        try:
            # Video second
            file = bot.getFile(msg.video.file_id)
            print('Found a video')
        except Exception:
            return

    now = datetime.datetime.now()
    if file != None:
        filename = 'img_' + str(now.hour) + '-' + str(now.minute) + '-' + str(
            now.second) + '-' + str(now.microsecond) + '.' + file.file_path.split('.')[-1]

        file.download(filename)

        uploadToDrive(filename, 'annee_' + str(now.year), monthNames[now.month - 1])

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
        bot = telegram.Bot(TOKEN)
        print('Listening ...')

        while 1:
            time.sleep(10)
            # Get all the messages read since last time
            try:
                updates = bot.get_updates(limit=1000, timeout=10, allowed_updates=['message'])

                for msg in updates:
                    handle(bot, msg.message)
            except Exception as e:
                print(e)