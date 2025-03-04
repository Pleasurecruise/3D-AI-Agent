import json
import time
import os
import ssl
import wave

import _thread as thread
from threading import Lock
from threading import Thread
from dotenv import load_dotenv
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from utils import logger
from gui.server import websocket
from gui.db.authorization import Authorization
from utils.thread_manager import MyThread

load_dotenv()
URL = "wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
AK_ID = os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"]
AK_SECRET = os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"]
APP_KEY = os.environ["ALIBABA_NLS_APP_KEY"]

__running = True
__my_thread = None
__token = ''

# 获取AccessToken
def _get_token():
    global _token
    __client = AcsClient(
        AK_ID,
        AK_SECRET,
        "cn-shanghai"
    )

    # 创建request，并设置参数。
    __request = CommonRequest()
    __request.set_method('POST')
    __request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    __request.set_version('2019-02-28')
    __request.set_action_name('CreateToken')
    response = json.loads(__client.do_action_with_exception(__request))
    _token = response['Token']['Id']
    authorization = Authorization()
    authorization_info = authorization.search_by_userid(APP_KEY)
    if authorization_info is not None:
        authorization.update(APP_KEY, _token, response['Token']['ExpireTime']*1000)
    else:
        authorization.insert(APP_KEY, _token, response['Token']['ExpireTime']*1000, int(time.time()*1000))

#   是否过期
def __runnable():
    while __running:
        _get_token()
        time.sleep(3600*12)

# 确保只有一个线程在运行
def start():
    MyThread(target=__runnable).start()

# Websocket连接
class AliyunASRStreaming:

    # 初始化
    def __init__(self, username):
        self.__URL = URL
        self.__ws = None
        self.__frames = []
        self.started = False
        self.__closing = False
        self.__task_id = ''
        self.done = False
        self.finalResults = ""
        self.username = username
        self.data = b'' #
        self.__endding = False
        self.__is_close = False
        self.lock = Lock()

    # 创建消息头
    def __create_header(self, name):
        if name == 'StartTranscription':
            self.__task_id = logger.random_hex(32)
        header = {
            "appkey": APP_KEY,
            "message_id": logger.random_hex(32),
            "task_id": self.__task_id,
            "namespace": "SpeechTranscriber",
            "name": name
        }
        return header

    # 收到websocket消息的处理
    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            header = data['header']
            name = header['name']
            if name == 'TranscriptionStarted':
                self.started = True
            if name == 'SentenceEnd':
                self.done = True
                self.finalResults = data['payload']['result']
                if websocket.get_web_instance().is_connected(self.username):
                    websocket.get_web_instance().add_cmd({"panelMsg": self.finalResults, "Username" : self.username})
                if websocket.get_instance().is_connected(self.username):
                    content = {'Topic': 'human', 'Data': {'Key': 'log', 'Value': self.finalResults}, 'Username' : self.username}
                    websocket.get_instance().add_cmd(content)
                ws.close()
            elif name == 'TranscriptionResultChanged':
                self.finalResults = data['payload']['result']
                if websocket.get_web_instance().is_connected(self.username):
                    websocket.get_web_instance().add_cmd({"panelMsg": self.finalResults, "Username" : self.username})
                if websocket.get_instance().is_connected(self.username):
                    content = {'Topic': 'human', 'Data': {'Key': 'log', 'Value': self.finalResults}, 'Username' : self.username}
                    websocket.get_instance().add_cmd(content)

        except Exception as e:
            print(e)

    # 收到websocket的关闭要求
    def on_close(self, ws, code, msg):
        self.__endding = True
        self.__is_close = True

    # 收到websocket错误的处理
    def on_error(self, ws, error):
        print("aliyun asr error:", error)
        self.started = True #避免在aliyun asr出错时，recorder一直等待start状态返回

    # 收到websocket连接建立的处理
    def on_open(self, ws):
        self.__endding = False
        #为了兼容多路asr，关闭过程数据
        def run(*args):
            while self.__endding == False:
                try:
                    if len(self.__frames) > 0:
                        with self.lock:
                            frame = self.__frames.pop(0)
                        if isinstance(frame, dict):
                            ws.send(json.dumps(frame))
                        elif isinstance(frame, bytes):
                            ws.send(frame, websocket.ABNF.OPCODE_BINARY)
                            self.data += frame
                    else:
                        time.sleep(0.001)  # 避免忙等
                except Exception as e:
                    print(e)
                    break
            if self.__is_close == False:
                for frame in self.__frames:
                    ws.send(frame, websocket.ABNF.OPCODE_BINARY)
                frame = {"header": self.__create_header('StopTranscription')}
                ws.send(json.dumps(frame))
        thread.start_new_thread(run, ())

    def __connect(self):
        self.finalResults = ""
        self.done = False
        with self.lock:
            self.__frames.clear()
        self.__ws = websocket.WebSocketApp(self.__URL + '?token=' + _token, on_message=self.on_message)
        self.__ws.on_open = self.on_open
        self.__ws.on_error = self.on_error
        self.__ws.on_close = self.on_close
        self.__ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def send(self, buf):
        with self.lock:
            self.__frames.append(buf)

    # 开始
    def start(self):
        Thread(target=self.__connect, args=[]).start()
        data = {
            'header': self.__create_header('StartTranscription'),
            "payload": {
                "format": "pcm",
                "sample_rate": 16000,
                "enable_intermediate_result": True,
                "enable_punctuation_prediction": False,
                "enable_inverse_text_normalization": True,
                "speech_noise_threshold": -1
            }
        }
        self.send(data)

    # 结束
    def end(self):
        self.__endding = True
        with wave.open('cache_data/input2.wav', 'wb') as wf:
            # 设置音频参数
            n_channels = 1  # 单声道
            sampwidth = 2   # 16 位音频，每个采样点 2 字节
            wf.setnchannels(n_channels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(16000)
            wf.writeframes(self.data)
        self.data = b''