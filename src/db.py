"""Various database related helpers."""

import asyncpg

from src import config
from src.models import WebsiteStatus

CREATE_WEBSITE_STATUS_TABLE_SQL = '''
    CREATE TABLE IF NOT EXISTS website_status (
        id bigserial PRIMARY KEY,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        response_time FLOAT NOT NULL,
        status_code INT NOT NULL,
        error_msg TEXT NOT NULL,
        regex TEXT NOT NULL,
        regex_passed BOOLEAN NOT NULL,
        checked_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
    )
'''

INSERT_WEBSITE_STATUS_SQL = '''
    INSERT INTO website_status (
        url,
        title,
        response_time,
        status_code,
        error_msg,
        regex,
        regex_passed,
        checked_at
    ) VALUES (
        $1::TEXT,
        $2::TEXT,
        $3::FLOAT,
        $4::INT,
        $5::TEXT,
        $6::TEXT,
        $7::BOOLEAN,
        $8::TIMESTAMP
    )
'''


async def get_conn() -> asyncpg.Connection:
    """Create a new database connection.

    :return: The newly created database connection.
    """
    return await asyncpg.connect(config.POSTGRE_DATABASE_URI)


async def init_db(conn: asyncpg.Connection):
    """Make sure all the tables are created.

    :param conn: The database connection to use.
    """
    await conn.execute(CREATE_WEBSITE_STATUS_TABLE_SQL)


async def insert_website_status(conn: asyncpg.Connection, website_status: WebsiteStatus):
    """Write the given website status into the database.

    :param conn: The database connection to use.
    :param website_status: The website status to write.
    """
    # User prepared statements for type validation.
    stmt = await conn.prepare(INSERT_WEBSITE_STATUS_SQL)
    await stmt.fetch(*website_status.dict().values())
