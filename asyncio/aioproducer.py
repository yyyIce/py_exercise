#!/usr/bin/python
#encoding:utf-8  

from aiokafka import AIOKafkaProducer
import asyncio
import json

async def produce():

    loop = asyncio.get_running_loop()
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        pkt = {
            "type": "test",
            "url":"http://test.com/"
        }
        await producer.send_and_wait("test3", pkt)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

async def main():
    task = asyncio.create_task(produce())
    await task

asyncio.run(main())