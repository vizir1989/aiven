from checker_kafka.kafka_producer.producer import CheckerProducer
from unittest.mock import MagicMock, patch


kafka_producer_config = ('checker', {'bootstrap_servers': 'kafka.aivencloud.com:18604'})


def test_checker_consumer():
    with patch('kafka.KafkaProducer', MagicMock):
        producer = CheckerProducer(kafka_producer_config)
        producer.send_message(200, 1234, ['test'])
        assert producer._CheckerProducer__producer.send.call_count == 1
        producer._CheckerProducer__producer.send.assert_called_with('checker',
            b'{"status_code": 200, "elapsed": 1234, "results": ["test"]}')
