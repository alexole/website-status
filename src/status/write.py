"""Check the status of a list of websites."""

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

from src import config
from src import db
from src.models import WebsiteStatus

logger = logging.getLogger(__name__)


async def write_website_status(run_forever: bool = True):
    """Write the collected website status data to the database.

    :param run_forever: Set the `False` to exit after all the events were processed.
    """
    # Initialize the database. Sadly, async context manager is not supported.
    conn = await db.get_conn()
    try:
        await db.init_db(conn)
        # Setup the Kafka consumer.
        consumer = AIOKafkaConsumer(
            config.WRITE_WEBSITE_STATUS_TOPIC,
            bootstrap_servers=config.KAFKA_URI,
            security_protocol='SSL',
            ssl_context=config.get_kafka_security_context(),
            group_id='write_websites_group'
        )
        async with consumer:
            while True:
                async for event in consumer:
                    # Get the website status.
                    website_status = WebsiteStatus(**json.loads(event.value.decode()))
                    # Write the status to the database.
                    await db.insert_website_status(conn, website_status)
                    logger.info(f'Saved status for website {website_status.url}')
                if not run_forever:
                    break
    finally:
        await conn.close()


if __name__ == '__main__':
    asyncio.run(write_website_status())
