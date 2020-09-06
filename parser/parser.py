from typing import List, Tuple
import logging

import requests
import re


def parse(url: str, patterns: List[str]) -> Tuple[int, int, List]:
    try:
        logging.info(f'start to request url {url}')
        with requests.get(url) as contents:
            page = contents.text
            status_code = contents.status_code
            elapsed = contents.elapsed
            result = []
            if page:
                logging.info('start to find info')
                for pattern in patterns:
                    result = re.findall(pattern, page)
            return status_code, elapsed.microseconds, result
    except requests.exceptions.MissingSchema as error:
        logging.error(error, exc_info=True)
        return -1, -1, []
