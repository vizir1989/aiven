from configuration.config import db_config
import psycopg2
from typing import List
import logging


class CheckerPostgres:
    _SQL_CREATE_TABLE = \
        """CREATE TABLE IF NOT EXISTS tbl_checker (
            request_id SERIAL PRIMARY KEY,
            url TEXT,
            pattern TEXT,
            status_code INT,
            elapsed INT,
            result TEXT,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)"""

    _SQL_RESULT_INSERT = \
        "INSERT INTO tbl_checker (url, pattern, status_code, elapsed, result) " \
        "VALUES (%s, %s, %s, %s, %s)"

    def __init__(self):
        logging.info('start to connect to postgres db')
        self.__connection = psycopg2.connect(**db_config())
        cursor = self.__connection.cursor()
        logging.info('start to create db')
        cursor.execute(CheckerPostgres._SQL_CREATE_TABLE)
        self.__connection.commit()
        logging.info('db created')

    def save(self, url: str, patterns: List[str], status_code: int, elapsed: int, results: List):
        logging.info('start to save message')
        cursor = self.__connection.cursor()
        cursor.execute(CheckerPostgres._SQL_RESULT_INSERT, (url, patterns, status_code, elapsed, results))
        self.__connection.commit()
        logging.info('message save')
