import json
import logging
from typing import Dict, Tuple

import kafka


class CheckerConsumer:
    """
    Represent kafka consumer
    """

    def __init__(self, db, main_config: Dict, kafka_config: Tuple[str, Dict]):
        """
        Create kafka consumer
        :param db: db for saving
        :param main_config: configuration with url and patterns
        :param kafka_config: configuration for kafka consumer
        """
        topic, config = kafka_config
        logging.info('connect to kafka consumer')
        self.__consumer = kafka.KafkaConsumer(topic, **config)
        self.__db = db
        cfg = main_config
        self.__url, self.__patterns = cfg['url'], cfg['patterns']

    def start(self):
        """
        Start consume kafka message
        """
        for message in self.__consumer:
            result = json.loads(message.value.decode('utf8'))
            logging.info(f"message: {result['status_code']}, {result['elapsed']}, {result['results']}")
            self.__db.save(url=self.__url, patterns=self.__patterns, **result)
