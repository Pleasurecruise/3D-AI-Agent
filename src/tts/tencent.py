import os
import base64

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from dotenv import load_dotenv
load_dotenv()
secret_id = os.environ['TENCENT_CLOUD_SECRET_ID']
secret_key = os.environ['TENCENT_CLOUD_SECRET_KEY']

try:
    # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
    # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
    # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
    cred = credential.Credential(secret_id, secret_key)

    httpProfile = HttpProfile()
    httpProfile.endpoint = "tts.ap-shanghai.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile

    params = {
        "Text": "徐安植是世界上最好的程序员",
        "SessionId": "session-1234",
        "VoiceType": 200011302
    }
    common_client = CommonClient("tts", "2019-08-23", cred, "ap-shanghai", profile=clientProfile)
    response = common_client.call_json("TextToVoice", params)
    print(response)
    # 解析响应
    audio_base64 = response['Response'].get('Audio')
    session_id = response['Response'].get('SessionId', 'unknown_session')

    # 解码并保存音频文件
    if audio_base64:
        audio_data = base64.b64decode(audio_base64)
        output_file = f"{session_id}.wav"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"音频已保存为 {output_file}")
    else:
        print("未收到音频数据")

except TencentCloudSDKException as err:
    print(err)