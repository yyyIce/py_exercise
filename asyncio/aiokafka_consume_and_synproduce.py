#!/usr/bin/python
#encoding:utf-8  
from aiokafka import AIOKafkaConsumer
from kafka import KafkaProducer
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

            producer.send('test7', data)
            print(f"{data['id']} produced at {time.strftime('%X')}")

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

async def main():

    loop = asyncio.get_running_loop()
    consumer = AIOKafkaConsumer(
        'test3',
        loop=loop, bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('ascii')))

    producer = KafkaProducer(
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                            bootstrap_servers='localhost:9092'
                        )

    consume_task = asyncio.create_task(consume(consumer, producer))
    await asyncio.gather(consume_task)

if __name__ == "__main__":
    print(f"started at {time.strftime('%X')}")
    asyncio.run(main())
    #print(f"finished at {time.strftime('%X')}")
