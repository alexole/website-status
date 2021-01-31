"""Shared logic across the status checker tests."""

from typing import NamedTuple


class KafkaEvent(NamedTuple):
    """A fake Kafka event."""

    value: bytes
