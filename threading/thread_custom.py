#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thread_custom.py
import threading
import time

#继承Thread类，创建自定义线程类
class mythread(threading.Thread):
    def __init__(self, num, threadname):
        threading.Thread.__init__(self, name=threadname)
        self.num = num

    #重写run()方法
    def run(self):
        while self.num > 0:
            print(f'{self.name}-minus {self.num}')
            self.num -= 1
            time.sleep(5)

t1 = mythread(3, 't1')
t1.start()


