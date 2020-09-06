from collections import namedtuple

from checker_kafka.kafka_consumer.consumer import CheckerConsumer
from unittest.mock import MagicMock, patch


main_config = {'url': 'https://test.com', 'patterns': ['test'], 'period': 10}
kafka_consumer_config = ('checker', {'bootstrap_servers': 'kafka.aivencloud.com:18604'})

message_count = 100


def message_generator(*args, **kwargs):
    Message = namedtuple('Message', ['value'])
    message = Message(bytes('{"status_code": 200, "elapsed": 1234, "results": ["test", "test"]}', encoding='utf8'))
    for i in range(message_count):
        yield message


def test_checker_consumer():
    my_db = MagicMock()
    with patch('kafka.KafkaConsumer', message_generator):
        consumer = CheckerConsumer(my_db, main_config, kafka_consumer_config)
        consumer.start()
        assert my_db.save.call_count == message_count
        my_db.save.assert_called_with(url='https://test.com', patterns=['test'], status_code=200, elapsed=1234,
                                      results=['test', 'test'])


