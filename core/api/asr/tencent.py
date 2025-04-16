import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models

class TencentASR:
    def __init__(self, secret_id, secret_key):
        self.cred = credential.Credential(secret_id, secret_key)
        self.http_profile = HttpProfile()
        self.http_profile.endpoint = "asr.tencentcloudapi.com"
        self.client_profile = ClientProfile()
        self.client_profile.http_profile = self.http_profile
        self.client = asr_client.AsrClient(self.cred, "ap-guangzhou", self.client_profile)

    def describe_task_status(self, params):
        try:
            req = models.CreateRecTaskRequest()
            req.from_json_string(json.dumps(params))
            resp = self.client.CreateRecTask(req)
            resp_dict = json.loads(resp.to_json_string())
            task_id = resp_dict.get("Data", {}).get("TaskId")
            return task_id
        except TencentCloudSDKException as err:
            print(err)
            return None

    def get_task_result(self, task_id):
        try:
            req = models.DescribeTaskStatusRequest()
            params = {"TaskId": task_id}
            req.from_json_string(json.dumps(params))
            resp = self.client.DescribeTaskStatus(req)
            return resp.to_json_string()
        except TencentCloudSDKException as err:
            print(err)
            return None