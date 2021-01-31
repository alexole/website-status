"""Tests for the website status check logic."""

from typing import NamedTuple
from unittest.mock import patch, AsyncMock

import httpx
import pytest

from src.collect.status import UNKNOWN_STATUS_CODE, UNKNOWN_RESPONSE_TIME, check_website_status, check_websites
from src.models import Website

# Mark all tests as coroutines.
pytestmark = pytest.mark.asyncio


class KafkaEvent(NamedTuple):
    """A fake Kafka event."""

    value: bytes


async def test_check_website_status(httpx_mock, website):
    """Test the simple website check successful path."""
    httpx_mock.add_response(method='GET', url=website.url)

    website_status = await check_website_status(website)

    assert website_status.status_code == 200
    assert website_status.url == 'https://foobar.com'


async def test_check_website_status_regex(httpx_mock, website):
    """Test the simple website check successful with regex path."""
    httpx_mock.add_response(method='GET', url=website.url, data='Lore ipsum foobar')
    website.regex = 'Foobar'

    website_status = await check_website_status(website)

    assert website_status.status_code == 200
    assert website_status.regex == 'Foobar'
    assert website_status.regex_passed


async def test_check_website_status_regex_error(httpx_mock, website):
    """"Test that the regex is not checked on non-successful responses."""
    httpx_mock.add_response(method='GET', url=website.url, status_code=404, data='Lore ipsum foobar')
    website.regex = 'Foobar'

    website = Website(**dict(
        url='https://foobar.com',
        title='Foo',
        regex='Foobar'
    ))
    website_status = await check_website_status(website)

    assert website_status.status_code == 404
    assert website_status.regex == 'Foobar'
    assert not website_status.regex_passed


@pytest.mark.parametrize('exception_cls, error_msg', [
    (httpx.TimeoutException, "Timeout error: TimeoutException('Error!')"),
    (httpx.NetworkError, "Network error: NetworkError('Error!')"),
    (httpx.HTTPError, "Unknown error: HTTPError('Error!')"),
])
async def test_check_website_status_timeout_error(exception_cls, error_msg, httpx_mock, website):
    """Test when a website check raises an error."""

    def _raise_timeout_error(request, ext):
        raise exception_cls('Error!', request=request)

    httpx_mock.add_callback(_raise_timeout_error)

    website_status = await check_website_status(website)

    assert website_status.status_code == UNKNOWN_STATUS_CODE
    assert website_status.response_time == UNKNOWN_RESPONSE_TIME
    assert website_status.error_msg == error_msg


@patch('src.db.get_conn', AsyncMock())
@patch('src.db.insert_website_status')
@patch('src.collect.status.AIOKafkaConsumer')
@patch('src.collect.status.check_website_status')
async def test_check_websites(mock_check_website_status, mock_kafka_consumer, mock_insert_website_status, website,
                              website_status):
    """Test the processing of website check events."""
    website_data_bytes = website.json().encode()
    mock_check_website_status.return_value = website_status
    mock_kafka_consumer.return_value.__aiter__.return_value = [
        KafkaEvent(value=website_data_bytes),
        KafkaEvent(value=website_data_bytes)
    ]

    await check_websites(run_forever=False)

    assert mock_check_website_status.await_count == 2
    assert mock_insert_website_status.await_count == 2
