#!/usr/bin/env python3
"""
Regex-ing
Log formatter
Create logger
Connect to secure database
Read and filter data
"""
import logging
import os
import re
from typing import List
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Define filter_datum"""
    for field in fields:
        message = re.sub(
                fr"{field}=.*?{separator}",
                f"{field}={redaction}{separator}", message
                )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Define format"""
        record.msg = filter_datum(
                self.fields, self.REDACTION,
                record.getMessage(), self.SEPARATOR
                )
        fields = record.msg.split(';')
        fields = [field.strip() for field in fields]
        record.msg = '; '.join(fields)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Define get_logger"""
    lg = logging.getLogger("user_data")
    lg.setLevel(logging.INFO)
    lg.propagate = False
    s = logging.StreamHandler()
    s.setFormatter(RedactingFormatter(PII_FIELDS))
    lg.addHandler(s)
    return lg


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Define get_db"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    ddatabase = os.getenv("PERSONAL_DATA_DB_NAME")
    db_connect = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
            )
    return db_connect


def main():
    """Define the main"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM users""")
    field_names = [i[0] for i in cursor.description]
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger = get_logger()
    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.log(logging.INFO, str_row.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
