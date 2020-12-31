#!/usr/bin/python
#encoding:utf-8  
from aiokafka import AIOKafkaConsumer
import asyncio
import json

async def consume(loop):
    consumer = AIOKafkaConsumer(
        'test3',
        loop=loop, bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('ascii')))
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

#loop.run_until_complete(consume())
async def main():
    loop = asyncio.get_running_loop()
    task = asyncio.create_task(consume(loop))
    await task

asyncio.run(main())

