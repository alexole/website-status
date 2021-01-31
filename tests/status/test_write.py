"""Tests for the website status writing logic."""

from unittest.mock import patch, AsyncMock

import pytest

from src.status.write import write_website_status

from tests.status.common import KafkaEvent

# Mark all tests as coroutines.
pytestmark = pytest.mark.asyncio


@patch('src.db.get_conn', AsyncMock())
@patch('src.status.write.AIOKafkaConsumer')
@patch('src.db.insert_website_status')
async def test_write_website_status(mock_insert_website_status, mock_kafka_consumer, website_status):
    """Test the processing of write website status events."""
    website_status_data_bytes = website_status.json().encode()
    mock_kafka_consumer.return_value.__aiter__.return_value = [
        KafkaEvent(value=website_status_data_bytes),
        KafkaEvent(value=website_status_data_bytes)
    ]

    await write_website_status(run_forever=False)

    assert mock_insert_website_status.await_count == 2
