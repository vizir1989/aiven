from checker_db.checker_postgres import CheckerPostgres
from typing import Union
from configuration.config import db_config


def db_create(db_name: str) -> Union[CheckerPostgres, None]:
    if db_name == 'ps':
        return CheckerPostgres(db_config())
    return None
