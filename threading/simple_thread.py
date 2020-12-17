#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# simple_thread.py
import time
from threading import Thread
def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

#注意args=(10,)的逗号不能省，不然不是tuple是int
t = Thread(target=countdown, args=(10,))
t.start()
