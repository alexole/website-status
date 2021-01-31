"""Trigger the status check for a list of websites."""

import asyncio
import json

from aiokafka import AIOKafkaProducer

from src import config
from src.models import Website


async def trigger_website_checks(config_json_filename: str):
    """Read the config file and trigger the website checks by writing a "check" event for each website.

    :param config_json_filename: The config file with all the websites to check.
    """
    with open(config_json_filename, mode='rt') as config_json_file:
        config_json = json.load(config_json_file)

    producer = AIOKafkaProducer(
        bootstrap_servers=config.KAFKA_URI,
        security_protocol='SSL',
        ssl_context=config.get_kafka_security_context()
    )
    async with producer:
        for website_config in config_json:
            website = Website(**website_config)
            await producer.send(config.CHECK_WEBSITES_TOPIC, website.json().encode())


if __name__ == '__main__':
    asyncio.run(trigger_website_checks(f'{config.SRC_ROOT}/../websites.json'))
