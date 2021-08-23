# (c) @AbirHasan2005

import os
from dotenv import load_dotenv

load_dotenv("configs.env")


class Config(object):
    API_ID = int(os.environ.get("API_ID", "123"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    STATUS_UPDATE_CHANNEL_ID = int(os.environ.get("STATUS_UPDATE_CHANNEL_ID", "-100"))
