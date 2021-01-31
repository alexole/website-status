"""Tests for the website status check triggering logic."""

from unittest.mock import patch, AsyncMock, mock_open

import pytest

from src.collect.trigger import trigger_website_checks

# Mark all tests as coroutines.
pytestmark = pytest.mark.asyncio


@patch('src.collect.trigger.AIOKafkaProducer')
async def test_trigger_website_checks(mock_kafka_producer, website):
    """Test the creation of website check events."""
    mock_kafka_producer.return_value = AsyncMock()
    json_data = '''
    [
        {
            "url": "https://www.google.com/sdf?q=python",
            "title": "Google",
            "regex": "Python"
        },
        {
            "url": "https://www.github.com",
            "title": "GitHub"
        }
    ]
    '''
    with patch('src.collect.trigger.open', mock_open(read_data=json_data.encode())):
        await trigger_website_checks('foobar.json')

    assert mock_kafka_producer.return_value.send.await_count == 2
