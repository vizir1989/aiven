import configuration.config
from unittest.mock import patch, mock_open
import pytest


test_yaml = """
kafka:
  bootstrap_services:
    - 'kafka.aivencloud.com:18604'
  ssl_cafile: 'keys/kafka_ca.pem'
  ssl_certfile: 'keys/kafka_service.cert'
  ssl_keyfile: 'keys/kafka_service.key'
  group_id: 'checker'
  client_id: 'checker'
  topic: 'checker'

celery:
  main: 'checker'
  broker_url: 'redis://test:test@redis.aivencloud.com:18602/0'
  backend_url: 'redis://test:test@redis.aivencloud.com:18602/1'

db:
  host: 'test.aivencloud.com'
  port: 18602
  user: 'test'
  password: 'test'
  sslrootcert: 'keys/postgres_ca.pem'
  database: 'defaultdb'
  connect_timeout: 5

sentry:
  dns: "https://sentry.io/5418763"

main:
  url: 'https://test.com'
  patterns:
    - 'test'
  period: 10
"""


def test_main_config():
    with patch('builtins.open', mock_open(read_data=test_yaml)):
        result = configuration.config.main_config()
        assert result == {'url': 'https://test.com', 'patterns': ['test'], 'period': 10}


def test_kafka_consumer_config():
    with patch('builtins.open', mock_open(read_data=test_yaml)):
        configuration.config.script_dir = ''
        result = configuration.config.kafka_consumer_config()
        assert result == ('checker', {'bootstrap_servers': 'kafka.aivencloud.com:18604', 'group_id': 'checker',
                                      'security_protocol': 'SSL', 'ssl_check_hostname': True,
                                      'ssl_cafile': 'keys/kafka_ca.pem',
                                      'ssl_certfile': 'keys/kafka_service.cert',
                                      'ssl_keyfile': 'keys/kafka_service.key'})


def test_kafka_producer_config():
    with patch('builtins.open', mock_open(read_data=test_yaml)):
        configuration.config.script_dir = ''
        result = configuration.config.kafka_producer_config()
        assert result == ('checker', {'bootstrap_servers': 'kafka.aivencloud.com:18604', 'client_id': 'checker',
                                      'security_protocol': 'SSL', 'ssl_check_hostname': True,
                                      'ssl_cafile': 'keys/kafka_ca.pem',
                                      'ssl_certfile': 'keys/kafka_service.cert',
                                      'ssl_keyfile': 'keys/kafka_service.key'})


def test_db_config():
    with patch('builtins.open', mock_open(read_data=test_yaml)):
        configuration.config.script_dir = ''
        result = configuration.config.db_config()
        assert result == {'host': 'test.aivencloud.com', 'database': 'defaultdb', 'user': 'test', 'password': 'test',
                          'port': 18602, 'sslrootcert': 'keys/postgres_ca.pem',
                          'connect_timeout': 5, 'sslmode': 'require'}


def test_celery_config():
    with patch('builtins.open', mock_open(read_data=test_yaml)):
        result = configuration.config.celery_config()
        assert result == {'main': 'checker', 'broker': 'redis://test:test@redis.aivencloud.com:18602/0',
                          'backend': 'redis://test:test@redis.aivencloud.com:18602/1'}


def test_sentry_config():
    with patch('builtins.open', mock_open(read_data=test_yaml)):
        result = configuration.config.sentry_config()
        assert result == {'dns': 'https://sentry.io/5418763'}


def test_main_fail():
    main_data = """
    main:
        patterns:
        - 'test'
        period: 10
  """
    with patch('builtins.open', mock_open(read_data=main_data)), pytest.raises(KeyError):
        configuration.config.main_config()


def test_main_with_out_patterns_success():
    main_data = """
    main:
        url: 'http://test.com'
        period: 10
  """
    with patch('builtins.open', mock_open(read_data=main_data)):
        configuration.config.main_config()


def test_kafka_producer_config_fail():
    kafka_data = """
        kafka:
          ssl_cafile: 'keys/kafka_ca.pem'
          ssl_certfile: 'keys/kafka_service.cert'
          ssl_keyfile: 'keys/kafka_service.key'
          group_id: 'checker'
          client_id: 'checker'
          topic: 'checker'
    """

    with patch('builtins.open', mock_open(read_data=kafka_data)), pytest.raises(KeyError):
        configuration.config.kafka_producer_config()


def test_kafka_consumer_config_fail():
    kafka_data = """
        kafka:
          ssl_cafile: 'keys/kafka_ca.pem'
          ssl_certfile: 'keys/kafka_service.cert'
          ssl_keyfile: 'keys/kafka_service.key'
          group_id: 'checker'
          client_id: 'checker'
          topic: 'checker'
    """

    with patch('builtins.open', mock_open(read_data=kafka_data)), pytest.raises(KeyError):
        configuration.config.kafka_consumer_config()


def test_celery_config_fail():
    celery_data = """
        celery:
          main: 'checker'
          backend_url: 'redis://test:test@redis.aivencloud.com:18602/1'
    """

    with patch('builtins.open', mock_open(read_data=celery_data)), pytest.raises(KeyError):
        configuration.config.celery_config()


def test_db_config_fail():
    db_data = """
        db:
          host: 'test.aivencloud.com'
          port: 18602
          user: 'test'
          password: 'test'
          sslrootcert: 'keys/postgres_ca.pem'
          connect_timeout: 5
    """

    with patch('builtins.open', mock_open(read_data=db_data)), pytest.raises(KeyError):
        configuration.config.db_config()


def test_sentry_config_fail():
    sentry_data = """
        sentry:
          test: 'test'
    """

    with patch('builtins.open', mock_open(read_data=sentry_data)), pytest.raises(KeyError):
        configuration.config.sentry_config()
