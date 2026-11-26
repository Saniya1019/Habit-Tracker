"""Creates the MySQL database automatically if it doesn't exist yet."""
import sys

import pymysql

from . import dbconfig as c


def ensure_database():
    try:
        conn = pymysql.connect(host=c.HOST, port=c.PORT, user=c.USER, password=c.PASSWORD)
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{c.NAME}` CHARACTER SET utf8mb4")
        conn.close()
    except Exception as e:
        sys.exit(
            f"\nCould not connect to MySQL at {c.HOST}:{c.PORT} as '{c.USER}'.\n"
            f"Reason: {e}\n\n"
            "Fix: make sure MySQL is running and that the user/password in config/dbconfig.py are correct.\n"
        )
