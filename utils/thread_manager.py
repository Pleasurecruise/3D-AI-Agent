import ctypes
import threading
from threading import Thread

class MyThread(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        add_thread(self)

    # 返回线程id
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        return next((id for id, thread in threading._active.items() if thread is self), None)

    # 强制停止线程
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

# 添加线程
def add_thread(thread: MyThread):
    if thread not in __thread_list:
        __thread_list.append(thread)

# 移除线程
def remove_thread(thread: MyThread):
    if thread in __thread_list:
        __thread_list.remove(thread)

# 停止所有线程
def stopAll():
    for thread in __thread_list:
        thread.raise_exception()
        thread.join()

__thread_list = []