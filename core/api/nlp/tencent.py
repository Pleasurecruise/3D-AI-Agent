import os
import json
from dotenv import load_dotenv
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

from gui.db.authorization import Authorization
from utils import logger

load_dotenv()
secret_id = os.environ['TENCENT_CLOUD_SECRET_ID']
secret_key = os.environ['TENCENT_CLOUD_SECRET_KEY']

def get_emotion(content):
    emotion = Emotion()
    answer = emotion.get_emotion(content)
    return answer

class Emotion:

    def __init__(self):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.authorization = Authorization()

    def get_emotion(self, content):
        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "nlp.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = nlp_client.NlpClient(cred, "", clientProfile)
            req = models.AnalyzeSentimentRequest()
            params = {
                "Text": content
            }
            req.from_json_string(json.dumps(params))
            resp = client.AnalyzeSentiment(req)
            response = json.loads(resp.to_json_string())
            if 'Sentiment' in response:
                return response['Sentiment']
            else:
                logger.log(1, f"腾讯情感分析对接有误： {response}")
                return 0
        except TencentCloudSDKException as err:
            logger.log(1, f"腾讯情感分析对接有误： {str(err)}")
            return 0