from typing import List, Tuple
import logging

import requests
import re


def parse(url: str, patterns: List[str]) -> Tuple[int, int, List]:
    """ requests target url and parse page with pattern

    :param url: target url
    :param patterns: list of regex

    :return: status code, elapsed time and found text
    """
    try:
        logging.info(f'start to request url {url}')
        with requests.get(url) as contents:
            page = contents.text
            status_code = contents.status_code
            elapsed = contents.elapsed
            if status_code == 200:
                result = []
                if page:
                    logging.info('start to find info')
                    for pattern in patterns:
                        for found in re.findall(pattern, page):
                            result.append(found)
                return status_code, elapsed.microseconds, result
            else:
                return status_code, elapsed.microseconds, []
    except requests.exceptions.RequestException as error:
        logging.error(error, exc_info=True)
        return 0, 0, []
