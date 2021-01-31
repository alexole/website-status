"""Global configuration."""

import os
import logging
from ssl import SSLContext

from aiokafka.helpers import create_ssl_context

logging.basicConfig(level=logging.INFO)


SRC_ROOT = os.path.abspath(os.path.dirname(__file__))

CHECK_WEBSITES_TOPIC = 'check_websites'
WRITE_WEBSITE_STATUS_TOPIC = 'write_website_status'

KAFKA_URI = os.environ['KAFKA_URI']
KAFKA_CA = os.path.join(SRC_ROOT, os.environ['KAFKA_CA'])
KAFKA_CERT = os.path.join(SRC_ROOT, os.environ['KAFKA_CERT'])
KAFKA_KEY = os.path.join(SRC_ROOT, os.environ['KAFKA_KEY'])

POSTGRE_DATABASE_URI = os.environ.get('POSTGRE_DATABASE_URI')


def get_kafka_security_context() -> SSLContext:
    """Get the security context required to connect to Kafka.

    :return: The security context required to connect to Kafka.
    """
    return create_ssl_context(cafile=KAFKA_CA, certfile=KAFKA_CERT, keyfile=KAFKA_KEY)
