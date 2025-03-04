import os

from dotenv import load_dotenv
from core.api.asr.aliyun import fileTrans

load_dotenv()
AK_ID = os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"]
AK_SECRET = os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"]
APP_KEY = os.environ["ALIBABA_NLS_APP_KEY"]

fileLink = "https://gw.alipayobjects.com/os/bmw-prod/0574ee2e-f494-45a5-820f-63aee583045a.wav"
fileTrans(AK_ID, AK_SECRET, APP_KEY, fileLink)