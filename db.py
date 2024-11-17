import psycopg2
from psycopg2 import sql, errors

from constants import DB_CONNECTION
from db_connect import DBConnect
from utils import ValidationError

db = DBConnect(**DB_CONNECTION)


def _add_cursor_wrapper(func):
    def wrapper(*args, **kwargs):
        with db.get_connection().cursor() as __cur:
            return func(__cur, *args, **kwargs)

    return wrapper


@_add_cursor_wrapper
def add_metric(__cur, tg_id, name):
    try:
        __cur.execute(
            """
                INSERT INTO metric (tg_id, name)
                VALUES (%s, %s)
            """,
            (tg_id, name)
        )
    except psycopg2.errors.UniqueViolation:
        raise ValidationError("Metric name already exists")


@_add_cursor_wrapper
def get_user_metrics(__cur, tg_id):
    __cur.execute(
        """
            SELECT uuid, name
            FROM metric
            WHERE tg_id = %s
            ORDER BY name ASC
        """,
        (tg_id,)
    )
    return __cur.fetchall()


@_add_cursor_wrapper
def add_stat(__cur, metric_uuid, value):
    __cur.execute(
        sql.SQL("""
            INSERT INTO stat (metric_uuid, value)
            VALUES (%s, %s)
        """),
        (metric_uuid, value)
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
    return __cur.fetchall()


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
    return __cur.fetchone()[0]
