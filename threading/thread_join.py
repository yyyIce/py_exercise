#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thread_join.py
import time
from threading import Thread
def countdown(n, id):
    while n > 0:
        print(f'T{id}-minus {n}')
        n -= 1
        time.sleep(5)

#注意args=(10,)的逗号不能省，不然不是tuple是int
t1 = Thread(target=countdown, args=(3,1))
t2 = Thread(target=countdown, args=(3,2))
t1.start()
t2.start()
#t1.join()
print("after join.")

