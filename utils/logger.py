import codecs
import os
import sys
import random
import time

from gui.server import websocket
from utils.thread_manager import MyThread

LOGS_FILE_URL = "logs/log-" + time.strftime("%Y%m%d%H%M%S") + ".log"

# 随机生成指定长度的十六进制字符串
def random_hex(length):
    result = hex(random.randint(0, 16 ** length)).replace('0x', '').lower()
    if len(result) < length:
        result = '0' * (length - len(result)) + result
    return result

# 写入日志文件
def __write_to_file(text):
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file = codecs.open(LOGS_FILE_URL, 'a', 'utf-8')
    file.write(text + "\n")
    file.close()

# 打印日志
def printInfo(level, sender, text, send_time=-1):
    if send_time < 0:
        send_time = time.time()
    format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(send_time)) + f".{int(send_time % 1 * 10)}"
    logStr = '[{}][{}] {}'.format(format_time, sender, text)
    print(logStr)
    if level >= 3:
        if websocket.get_web_instance().is_connected(sender):
            websocket.get_web_instance().add_cmd({"panelMsg": text} if sender == "系统" else {"panelMsg": text, "Username" : sender})
        if websocket.get_instance().is_connected(sender):
            content = {'Topic': 'human', 'Data': {'Key': 'log', 'Value': text}} if sender == "系统" else  {'Topic': 'human', 'Data': {'Key': 'log', 'Value': text}, "Username" : sender}
            websocket.get_instance().add_cmd(content)
        MyThread(target=__write_to_file, args=[logStr]).start()

# 打印系统日志
def log(level, text):
    printInfo(level, "系统", text)

class DisablePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout