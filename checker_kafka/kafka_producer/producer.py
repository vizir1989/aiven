import json
from typing import List, Tuple, Dict
import kafka
import logging


class CheckerProducer:
    """
    Represent producer. Send message in kafka
    """

    def __init__(self, kafka_producer_config: Tuple[str, Dict]):
        """
        Create kafka producer
        :param kafka_producer_config: topic and configuration for kafka
        """
        topic, config = kafka_producer_config
        self.__topic = topic
        self.__producer = kafka.KafkaProducer(**config)

    def send_message(self, status_code: int, elapsed: int, results: List):
        """
        Send message in kafka

        :param status_code: status code for target page
        :param elapsed: elapsed time in microseconds
        :param results: found text
        """
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
