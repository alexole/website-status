"""Shared test data for the package."""

from datetime import datetime

import pytest

from src.models import Website, WebsiteStatus


@pytest.fixture
def website() -> Website:
    return Website(**dict(
        url='https://foobar.com',
        title='Foo'
    ))


@pytest.fixture
def website_status() -> WebsiteStatus:
    return WebsiteStatus(**dict(
        url='https://foobar.com',
        title='Foo',
        response_time=0.5,
        status_code=200,
        error_msg='',
        regex='',
        regex_passed=False,
        checked_at=datetime.now()
    ))
