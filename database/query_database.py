import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "product_analytics.db"
)


def execute_query(sql):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(sql)

        results = cursor.fetchall()

        column_names = [
            description[0]
            for description in cursor.description
        ]

        return results, column_names

    finally:
        connection.close()