import os
import time
import json
from dotenv import load_dotenv
from utils.base64 import AudioBase64Util
from core.api.asr.tencent import TencentASR
load_dotenv()

def main():
    secret_id = os.getenv("TENCENT_CLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENT_CLOUD_SECRET_KEY")

    audio_file_path = "../assets/asr/zh.wav"
    base64_data = AudioBase64Util.audio_to_base64(audio_file_path)

    params = {
        "EngineModelType": "16k_zh",
        "ChannelNum": 1,
        "ResTextFormat": 0,
        "SourceType": 1,
        "Data": base64_data,
    }

    tencent_asr = TencentASR(secret_id, secret_key)
    task_id = tencent_asr.describe_task_status(params)
    print(task_id)

    while True:
        result_json = tencent_asr.get_task_result(task_id)
        result = json.loads(result_json)
        print(result)
        if result.get("Data", {}).get("Status") == 2:
            break
        time.sleep(5)
    print(result.get("Data", {}).get("Result"))
    return result.get("Data", {}).get("Result")

if __name__ == "__main__":
    main()
