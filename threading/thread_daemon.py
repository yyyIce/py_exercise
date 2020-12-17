#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thread_daemon.py
import time
from threading import Thread
def countdown(n, id):
    while n > 0:
        print(f'T{id}-minus {n}')
        n -= 1
        time.sleep(5)

#t1 = Thread(target=countdown, args=(3,1), daemon=False)
t1 = Thread(target=countdown, args=(3,1), daemon=True)
t1.start()
print("Main Thread End.")

