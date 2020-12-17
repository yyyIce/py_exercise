#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thread_queue.py
import time,random
import queue,threading
q = queue.Queue()
 
def producer(name):
    count = 0
    while count < 20:
        time.sleep(random.randrange(3))
        q.put(count)  # 生产item到队列
        print('Producer %s has produced %s item..' % (name, count))
        count += 1


def consumer(name):
    count = 0  
    while count < 20:
        time.sleep(random.randrange(4))
        if not q.empty():  # 如果还有item
            data = q.get()  # 就继续获取item
            #'\033[显示方式;前景色;背景色m<输出内容>\033[0m'输出有文字颜色和背景色的内容，其中'\033[0m'表示该颜色结束
            print('\033[32;1mConsumer %s has eat %s item...\033[0m' % (name, data))
            count += 1
            q.task_done()
        else:
            print("waiting...")
 
p1 = threading.Thread(target=producer, args=('A',))
c1 = threading.Thread(target=consumer, args=('B',))
p1.start()
c1.start()
q.join()

