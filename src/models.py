"""Data model shared between the """

from datetime import datetime

from pydantic import BaseModel, HttpUrl


class Website(BaseModel):
    """Represents a website to check the status for.

    If `regex` is set, the response content will be checked against it.
    """

    url: HttpUrl
    title: str
    regex: str = ''


class WebsiteStatus(BaseModel):
    """Represents the result of a status check for a website."""

    url: HttpUrl
    title: str
    response_time: float
    status_code: int
    error_msg: str
    regex: str
    regex_passed: bool
    checked_at: datetime
