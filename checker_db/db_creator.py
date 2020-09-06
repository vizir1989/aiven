from typing import Union

from checker_db.checker_postgres import CheckerPostgres
from configuration.config import db_config


def db_create(db_name: str) -> Union[CheckerPostgres, None]:
    """
    Create db.
    :param db_name: db name. Allowed values: 'ps' - posgresql
    :return: CheckerPostgres or None
    """
    if db_name == 'ps':
        return CheckerPostgres(db_config())
    return None
