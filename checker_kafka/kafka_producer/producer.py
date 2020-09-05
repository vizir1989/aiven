import json
from typing import List
from kafka import KafkaProducer
from configuration.config import kafka_producer_config
import logging


class CheckerProducer:

    def __init__(self):
        # TODO on_delivery
        topic, config = kafka_producer_config()
        self.__topic = topic
        self.__producer = KafkaProducer(**config)

    def send_message(self, status_code: int, elapsed: int, results: List):
        try:
            message = json.dumps({
                'status_code': status_code,
                'elapsed': elapsed,
                'results': results
            })

            self.__producer.send(self.__topic, bytes(message, encoding='utf8')).add_callback(
                self.__on_send_success).add_errback(self.__on_send_error)
            self.__producer.flush()
        except Exception as error:
            logging.error(error)

    @staticmethod
    def __on_send_error(excp: bool):
        logging.error('error', exc_info=excp)

    @staticmethod
    def __on_send_success(*args, **kwargs):
        logging.info('producer send message')
