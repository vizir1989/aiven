from checker_db.checker_postgres import CheckerPostgres
from typing import Union


def db_create(db_name: str) -> Union[CheckerPostgres, None]:
    if db_name == 'ps':
        return CheckerPostgres()
    return None
