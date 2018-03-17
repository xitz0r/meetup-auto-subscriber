FROM python:3-onbuild
CMD [ "python", "./meetup_helper.py", "TELEGRAM_BOT_API_KEY", "TELEGRAM_CHANNEL_ID", "MEETUP_GROUP_NAME" ]