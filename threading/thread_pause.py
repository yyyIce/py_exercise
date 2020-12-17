#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thread_pause.py
import threading
import time

class myThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()                   
        self.__running = threading.Event()  # 用于结束线程的标识
        self.__running.set()               

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()              # 如果__flag=False则阻塞
            print(time.time())
            time.sleep(1)

    def pause(self):
        self.__flag.clear()                 # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()                   # 设置为True, 唤醒线程

    def stop(self):
        self.__flag.set()                   # 如果线程暂停则先恢复
        self.__running.clear()              # 设置为False

a = myThread()
a.start()
time.sleep(3)
a.pause()
time.sleep(5)
a.resume()
time.sleep(3)
a.pause()
time.sleep(2)
a.stop()