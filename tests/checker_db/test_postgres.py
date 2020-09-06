from checker_db.checker_postgres import CheckerPostgres
from unittest.mock import MagicMock, patch


db_config = {'host': 'test.aivencloud.com', 'database': 'defaultdb', 'user': 'test', 'password': 'test',
             'port': 18602}


def test_postgres():
    # TODO use pytest-postgresql
    with patch('psycopg2.connect', MagicMock):
        checker = CheckerPostgres(db_config)
        checker.save('http://test.com', ['test'], 200, 1234, ['test'])
