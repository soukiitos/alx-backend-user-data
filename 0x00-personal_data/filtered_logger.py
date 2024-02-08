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
                fr"{field}=,*?{separator}",
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
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
            )
    return cnx


def main():
    """Define the main"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT CONCAT(
            'name=', name, ';ssn=', ssn, ';ip=', ip,
            ';user_agent=', user_agent, ';'
            ) AS message FROM users""")
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger = get_logger()
    for user in cursor:
        logger.log(logging.INFO, user[0])
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
