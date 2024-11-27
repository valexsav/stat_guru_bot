from decimal import Decimal

from psycopg2 import sql

from constants import DB_CONNECTION
from db_connect import DBConnect
from encrypt import (
    encrypt_data,
    decrypt_data,
)

db = DBConnect(**DB_CONNECTION)


def _add_cursor_wrapper(func):
    def wrapper(*args, **kwargs):
        with db.get_connection().cursor() as __cur:
            return func(__cur, *args, **kwargs)

    return wrapper


@_add_cursor_wrapper
def add_metric(__cur, chat_id, name):
    __cur.execute(
        """
            INSERT INTO metric (chat_id, name)
            VALUES (%s, %s)
        """,
        (chat_id, encrypt_data(name))
    )


@_add_cursor_wrapper
def get_user_metrics(__cur, chat_id):
    __cur.execute(
        """
            SELECT uuid, name
            FROM metric
            WHERE chat_id = %s
            ORDER BY name ASC
        """,
        (chat_id,)
    )
    return tuple(
        (row[0], decrypt_data(bytes(row[1])))
        for row in __cur.fetchall()
    )


@_add_cursor_wrapper
def add_stat(__cur, chat_id, metric_uuid, value):
    __cur.execute(
        sql.SQL("""
            INSERT INTO stat (metric_uuid, value)
            VALUES (%s, %s)
        """),
        (metric_uuid, encrypt_data(str(value)))
    )


@_add_cursor_wrapper
def get_stats(__cur, metric_uuid):
    __cur.execute(
        """
            SELECT value, created_at
            FROM stat
            WHERE metric_uuid = %s
            order BY created_at DESC
        """,
        (metric_uuid,),
    )
    return tuple(
        (Decimal(decrypt_data(bytes(row[0]))), row[1])
        for row in __cur.fetchall()
    )


@_add_cursor_wrapper
def get_metric_name(__cur, metric_uuid):
    __cur.execute(
        """
            SELECT name
            FROM metric
            WHERE uuid = %s
        """,
        (metric_uuid,),
    )
    return decrypt_data(bytes(__cur.fetchone()[0]))
