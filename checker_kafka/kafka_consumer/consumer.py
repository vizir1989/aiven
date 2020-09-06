import kafka
import json
import logging
from typing import Dict, Tuple, List


class CheckerConsumer:

    def __init__(self, db, main_config: Dict, kafka_config: Tuple[str, Dict]):
        topic, config = kafka_config
        logging.info('connect to kafka consumer')
        self.__consumer = kafka.KafkaConsumer(topic, **config)
        self.__db = db
        cfg = main_config
        self.__url, self.__patterns = cfg['url'], cfg['patterns']

    def start(self):
        for message in self.__consumer:
            result = json.loads(message.value.decode('utf8'))
            logging.info(f"message: {result['status_code']}, {result['elapsed']}, {result['results']}")
            self.__db.save(url=self.__url, patterns=self.__patterns, **result)
