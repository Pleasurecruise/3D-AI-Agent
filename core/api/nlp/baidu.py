import os
import time
import json
import requests

from dotenv import load_dotenv
from gui.db.authorization import Authorization
from utils import logger

load_dotenv()
app_id = os.environ['BAIDU_NLS_APP_ID']
api_key = os.environ['BAIDU_CLOUD_API_KEY']
secret_key = os.environ['BAIDU_CLOUD_SECRET_KEY']

def get_emotion(content):
    emotion = Emotion()
    answer = emotion.get_emotion(content)
    return answer

class Emotion:

    def __init__(self):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.authorization = Authorization()

    def get_emotion(self, content):
        token = self.__check_token()
        if token is None or token == 'expired':
            token_info = self.__get_token()
            if token_info is not None and token_info['access_token'] is not None:
                # 转换过期时间
                updated_at = time.time()
                create_time = int(updated_at * 1000)
                expires_time = token_info['expires_in']
                expiry_timestamp_in_seconds = updated_at + expires_time
                expiry_timestamp_in_milliseconds = expiry_timestamp_in_seconds * 1000
                if token == 'expired':
                    self.authorization.update(self.app_id, token_info['access_token'], expiry_timestamp_in_milliseconds)
                else:
                    self.authorization.insert(self.app_id, token_info['access_token'], expiry_timestamp_in_milliseconds, create_time)
                token = token_info['access_token']
            else:
                token = None

        if token is not None:
            try:
                url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={token}"
                request = json.dumps({"text": content})
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                response = requests.post(url, headers=headers, data=request)
                if response.status_code != 200:
                    logger.log(1, f"百度情感分析对接有误: {response.text}")
                    return 0
                info = json.loads(response.text)
                if 'error_code' not in info:
                    return info['items'][0]['sentiment']
                else:
                    logger.log(1, f"百度情感分析对接有误： {info['error_msg']}")
                    return 0
            except Exception as e:
                logger.log(1, f"百度情感分析对接有误： {str(e)}")
                return 0
        else:
            return 0

    # 获取AccessToken
    def __get_token(self):
        try:
            url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={api_key}&client_secret={secret_key}&grant_type=client_credentials"
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            r = requests.post(url, headers=headers)
            if r.status_code != 200:
                info = json.loads(r.text)
                if info["error"] == "invalid_client":
                    logger.log(1, f"请检查baidu_emotion_api_key")
                else:
                    logger.log(1, f"请检查baidu_emotion_secret_key")
                return None
            info = json.loads(r.text)
            if 'error_code' not in info:
                return info
            else:
                logger.log(1, f"百度情感分析对接有误： {info['error_msg']}")
                logger.log(1, f"请检查baidu_emotion_api_key和baidu_emotion_secret_key")
                return None
        except Exception as e:
            logger.log(1, f"百度情感分析有1误： {str(e)}")
            return None

    # 检查AccessToken
    def __check_token(self):
        self.authorization.init_db()
        info = self.authorization.search_by_userid(self.app_id)
        if info is not None:
            if int(info[1]) >= int(time.time()) * 1000:
                return info[0]
            else:
                return 'expired'
        else:
            return None