#!/usr/bin/python
#encoding:utf-8  
# aiokafka_to_s3.py
import json
import time
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import base64
import aiohttp
from aiohttp import ClientSession

headers = {
            "Content-Type":"pcapng", 
            "token":"c21f969b5f03d33d43e04f8f136e7682"
        }
endpoint_url = 'http://192.168.40.223:9098/hos/test7/'

with open('test.pcapng', 'rb') as f:
    pcapng_data = f.read()

total_s3 = 0
total_prod = 0

async def produce(producer, msg):
    # Get cluster layout and initial topic/partition leadership information
    try:
        await producer.send_and_wait("test6", msg)
        #print(f"INFO: {time.strftime('%X')} {msg['id']} produced. ")
    except:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

async def consume(consumer, producer, msg_q):
    # Get cluster layout and join group `my-group`
    global total_prod
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            
            data = msg.value

            data.pop('type')
            data['id'] = total_prod
            data['url'] = endpoint_url + str(data['id']) + '.pcapng'
            
            await produce(producer, data)

            # json中不能有byte类型
            data['pcapng'] = pcapng_data
            await msg_q.put(data)

            total_prod += 1

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

async def upload_to_s3(session,semaphore,queue):
    global total_s3
    while True:
        data = await queue.get()
        url = data['url']
        async with semaphore:
            async with session.put(url,data=data['pcapng'],headers=headers) as resp:
                if resp.status == 200:
                    queue.task_done()
                    total_s3 += 1
                    #print(f"INFO: {time.strftime('%X')} finish upload {data['id']} {url}. ")
                else:
                    # 此处错误没有做重传处理，可以采用再放回队列的方式
                    print(f"ERROR: {time.strftime('%X')} {resp.status} {url}. Retried. ")
                

async def print_metric(start_time):
    while True:
        t_time = time.time() - start_time
        s3_speed = total_s3/t_time
        prod_speed = total_prod/t_time
        print(f"upload to s3: {s3_speed}")
        print(f"produce to kafka: {prod_speed}")
        await asyncio.sleep(1)

async def main():
    #初始化工作
    pcapng_q = asyncio.Queue(500)
    semaphore =asyncio.Semaphore(500)
    start_time = time.time()
    async with ClientSession() as session:
        loop = asyncio.get_running_loop()
        consumer = AIOKafkaConsumer(
            'test3',
            loop=loop, bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('ascii')))

        producer = AIOKafkaProducer(
            loop=loop, bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        await producer.start()

        consume_task = asyncio.create_task(consume(consumer, producer, pcapng_q))
        speed_task = asyncio.create_task(print_metric(start_time))
        
        print(f"started {time.strftime('%X')}")
       
        tasks_s3 = []
        for i in range(100):
            tasks_s3.append(asyncio.create_task(upload_to_s3(session,semaphore,pcapng_q)))
        
        await pcapng_q.join()
        await asyncio.gather(consume_task, speed_task, *tasks_s3)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Quit.") 
    
