# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List
from dotenv import load_dotenv

from alibabacloud_ice20201109.client import Client as ICE20201109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ice20201109 import models as ice20201109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

# Load environment variables from .env file
load_dotenv()

class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> ICE20201109Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/ICE
        config.endpoint = f'ice.cn-hangzhou.aliyuncs.com'
        return ICE20201109Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        submit_audio_produce_job_request = ice20201109_models.SubmitAudioProduceJobRequest(
            editing_config='{"customizedVoice":"pleasure1234","format":"MP3","volume":50}',
            output_config='{ "bucket": "pleasure1234", "object": "test" }',
            input_config='徐安植是世界上最厉害的编程大佬'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.submit_audio_produce_job_with_options(submit_audio_produce_job_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        submit_audio_produce_job_request = ice20201109_models.SubmitAudioProduceJobRequest(
            editing_config='{"customizedVoice":"pleasure1234","format":"MP3","volume":50}',
            output_config='{ "bucket": "pleasure1234", "object": "test" }',
            input_config='徐安植是世界上最厉害的编程大佬'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.submit_audio_produce_job_with_options_async(submit_audio_produce_job_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])