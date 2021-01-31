"""Check the status of a list of websites."""

import asyncio
from datetime import datetime
import json
import logging
import re

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import httpx

from src import config
from src.models import Website, WebsiteStatus

logger = logging.getLogger(__name__)

UNKNOWN_STATUS_CODE = -1
UNKNOWN_RESPONSE_TIME = -1.0


async def check_website_status(website: Website) -> WebsiteStatus:
    """Check the status of the given website.

    :param website: The website to check.
    :return: The result of the website status check.
    """
    regex_passed = False
    response_time = UNKNOWN_RESPONSE_TIME
    status_code = UNKNOWN_STATUS_CODE
    error_msg = ''
    try:
        async with httpx.AsyncClient(http2=True) as client:
            resp = await client.get(website.url)

        response_time = resp.elapsed.total_seconds()
        status_code = resp.status_code

        if website.regex and resp.status_code == 200:
            # We need to check the content against the given pattern.
            regex_passed = bool(re.search(website.regex, resp.text, flags=re.IGNORECASE))
    except httpx.TimeoutException as timeout_exc:
        error_msg = str(f'Timeout error: {timeout_exc!r}')
    except httpx.NetworkError as network_exc:
        error_msg = str(f'Network error: {network_exc!r}')
    except httpx.HTTPError as http_exc:
        error_msg = str(f'Unknown error: {http_exc!r}')

    logger.info(f'Checked status for website {website}')

    return WebsiteStatus(
        url=website.url,
        title=website.title,
        response_time=response_time,
        status_code=status_code,
        error_msg=error_msg,
        regex=website.regex,
        regex_passed=regex_passed,
        checked_at=datetime.now()
    )


async def check_websites(run_forever: bool = True):
    """Listen to the event stream for any website check events.

    :param run_forever: Set the `False` to exit after all the events were processed.
    """
    # Setup the Kafka consumer.
    consumer = AIOKafkaConsumer(
        config.CHECK_WEBSITES_TOPIC,
        bootstrap_servers=config.KAFKA_URI,
        security_protocol='SSL',
        ssl_context=config.get_kafka_security_context(),
        group_id='check_websites_group'
    )
    producer = AIOKafkaProducer(
        bootstrap_servers=config.KAFKA_URI,
        security_protocol='SSL',
        ssl_context=config.get_kafka_security_context()
    )
    async with consumer, producer:
        while True:
            async for event in consumer:
                # Get the website status.
                website = Website(**json.loads(event.value.decode()))
                website_status = await check_website_status(website)
                # Write the status to the write status event stream.
                await producer.send(config.WRITE_WEBSITE_STATUS_TOPIC, website_status.json().encode())
            if not run_forever:
                break


if __name__ == '__main__':
    asyncio.run(check_websites())
