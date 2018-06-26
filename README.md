# uploadBot
A telegram bot in python which upload the photos on Google Drive in a group conversation.

# How to use
## Download
* Get the project with `git clone https://github.com/coignetp/uploadBot.git`
* Install everything with `pip3 install -r requirements.txt`
* Rename the *config.json.template* to *config.json*

## Create the Telegram bot
* Talk to **@botfather** on telegram with `/newbot` command
* Follow the instruction
* At the end **@botfather** will give you a token like *110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw*. Copy it and paste it in your *config.json* at the *tg_token*.

If you want your bot to upload every pictures on a group conversation (not only those sent to it), turn off the privacy mode with talking to **@botfather**

## Link it with google drive
* Follow https://developers.google.com/drive/api/v3/quickstart/python from step 1.a to 1.g
* Rename the downloaded file *client_secrets.json* and put it at the root folder
* Change *ggd_folder* in the *config.json* and give the folder where you want to put every photos

## Start
Now you can start the bot with `python3 botTG.py`.
Please note that the first time a photo will be uploaded, you will have to login to google. Your credentials will be saved for the next time in creds.txt and the login will be automatic.
