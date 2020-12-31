#!/usr/bin/python
#encoding:utf-8  
from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
import asyncio
import json
import time
import base64

async def consume(consumer, producer):
    # Get cluster layout and join group `my-group`
    count = 0
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:

            count += 1
            data = msg.value
            data.pop('type')
            data['id'] = count

            await produce(producer, data)

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

async def produce(producer, msg):
    # Get cluster layout and initial topic/partition leadership information
    
    try:
        await producer.send_and_wait("test7", msg)
        print(f"{msg['id']} produced at {time.strftime('%X')}")
    except:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

async def main():
    
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

    consume_task = asyncio.create_task(consume(consumer, producer))
    await asyncio.gather(consume_task)

if __name__ == "__main__":
    print(f"started at {time.strftime('%X')}")
    asyncio.run(main())
    #print(f"finished at {time.strftime('%X')}")
