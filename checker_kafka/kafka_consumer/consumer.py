from kafka import KafkaConsumer
from configuration.config import kafka_consumer_config, main_config
import json
import logging


class CheckerConsumer:

    def __init__(self, db):
        topic, config = kafka_consumer_config()
        logging.info('connect to kafka consumer')
        self.__consumer = KafkaConsumer(topic, **config)
        self.__db = db
        self.__url, self.__patterns = main_config()

    def start(self):
        for message in self.__consumer:
            result = json.loads(message.value.decode('utf8'))
            logging.info(f'message: {result}'.format(result))
            self.__db.save(url=self.__url, patterns=self.__patterns, **result)
