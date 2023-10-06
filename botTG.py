import time
import telegram
import logging
import datetime
import os
import json
import google_drive_util  # Import the Drive class from the previous refactored code

# For the French version. Can be changed.
monthNames = [
    "01 - Janvier",
    "02 - Fevrier",
    "03 - Mars",
    "04 - Avril",
    "05 - Mai",
    "06 - Juin",
    "07 - Juillet",
    "08 - Aout",
    "09 - Septembre",
    "10 - Octobre",
    "11 - Novembre",
    "12 - Decembre",
    "Inconnu",
]

logger = logging.getLogger(__name__)

def getFolder(drive, yearfold, monthfold):
    foldersY = drive.find_folders(yearfold)

    if len(foldersY) == 0:
        foldersY.append(drive.create_subfolder(MainFolder, yearfold))

    foldersM = drive.find_folders(monthfold)

    for f in foldersM:
        if f.get('parents')[0].get('id') == foldersY[-1].get('id'):
            return f

    return drive.create_subfolder(foldersY[-1], monthfold)

def handle(drive, bot, msg):
    file = None

    try:
        # Try photo first
        best_id = 0
        for i in range(len(msg.photo)):
            if msg.photo[best_id].file_size < msg.photo[i].file_size:
                best_id = i
        file = bot.getFile(msg.photo[best_id].file_id)
        logger.debug(f"Found a photo: {file.file_size}")
    except Exception:
        try:
            # Video second
            file = bot.getFile(msg.video.file_id)
            logger.debug(f"Found a video: {file.file_size}")
        except Exception:
            return

    now = datetime.datetime.now()
    if file is not None:
        filename = f"img_{now.hour}-{now.minute}-{now.second}-{now.microsecond}"
        filename += file.file_path.split(".")[-1]

        file.download(filename)

        year_folder = "annee_" + str(now.year)
        month_folder = monthNames[now.month - 1]
        
        drive.upload_files_to_folder([filename], getFolder(drive, year_folder, month_folder))

        os.remove(filename)

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)

    with open("config.json") as jsonfile:
        config = json.load(jsonfile)
        drive = google_drive_util.Drive()

        TOKEN = config["tg_token"]
        FOLDER = config["ggd_folder"]

        # The bot is ready to start
        bot = telegram.Bot(TOKEN)
        logger.debug("Listening ...")

        update_id = 0

        while 1:
            time.sleep(10)
            # Get all the messages read since the last time
            try:
                updates = bot.get_updates(
                    offset=update_id,
                    limit=1000,
                    timeout=10,
                    allowed_updates=["message"],
                )
                logger.debug("Found {} update(s)".format(len(updates)))

                for msg in updates:
                    handle(drive, bot, msg.message)
                    update_id = msg.update_id + 1

            except Exception as e:
                logger.debug(e)
