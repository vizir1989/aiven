import yaml
import os
from typing import Dict, Tuple

script_dir = os.path.dirname(__file__) + '/'


def kafka_producer_config() -> Tuple[str, Dict]:
    """
    Get configuration for kafka producer
    NOTE: bootstrap_services, topic, ssl_cafile, ssl_certfile, ssl_keyfile required.
    :return: tuple topic and dict with configuration
    """
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        kafka_cfg = cfg['kafka']
        result = {
            'bootstrap_servers': ','.join(kafka_cfg['bootstrap_services']),
            'client_id': kafka_cfg.get('client_id', None),
            'security_protocol': 'SSL',
            'ssl_check_hostname': True,
            'ssl_cafile': script_dir + kafka_cfg['ssl_cafile'],
            'ssl_certfile': script_dir + kafka_cfg['ssl_certfile'],
            'ssl_keyfile': script_dir + kafka_cfg['ssl_keyfile']
        }
        topic = kafka_cfg['topic']
        return topic, result


def kafka_consumer_config() -> Tuple[str, Dict]:
    """
    Get configuration for kafka consumer
    NOTE: bootstrap_services, topic, ssl_cafile, ssl_certfile, ssl_keyfile required.
    :return: tuple topic and dict with configuration
    """
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        kafka_cfg = cfg['kafka']
        result = {
            'bootstrap_servers': ','.join(kafka_cfg['bootstrap_services']),
            'group_id': kafka_cfg.get('group_id', None),
            'security_protocol': 'SSL',
            'ssl_check_hostname': True,
            'ssl_cafile': script_dir + kafka_cfg['ssl_cafile'],
            'ssl_certfile': script_dir + kafka_cfg['ssl_certfile'],
            'ssl_keyfile': script_dir + kafka_cfg['ssl_keyfile']
        }
        topic = kafka_cfg['topic']
        return topic, result


def celery_config() -> Dict:
    """
    Get configuration for celery
    NOTE: main, broker and backend_url required.
    :return: dict with configuration
    """
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        celery_cfg = cfg['celery']
        result = {
            'main': celery_cfg['main'],
            'broker': celery_cfg['broker_url'],
            'backend': celery_cfg['backend_url'],
        }
        return result


def db_config() -> Dict:
    """
    Get configuration for db
    NOTE: host, database, user, password, port, sslrootcert, connect_timeout required.
    :return: dict with configuration
    """
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        db_cfg = cfg['db']
        result = {
            'host': db_cfg['host'],
            'database': db_cfg['database'],
            'user': db_cfg['user'],
            'password': db_cfg['password'],
            'port': db_cfg['port'],
            'sslrootcert': script_dir + db_cfg['sslrootcert'],
            'connect_timeout': db_cfg['connect_timeout'],
            'sslmode': 'require'
        }
        return result


def sentry_config() -> Dict:
    """
    Get configuration for sentry
    NOTE: dns required.
    :return: dict with configuration
    """
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        sentry_cfg = cfg['sentry']
        result = {
            'dns': sentry_cfg['dns']
        }
        return result


def main_config() -> Dict:
    """
    Get main configuration
    NOTE: url and period required.
    :return: dict with configuration
    """
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        main_cfg = cfg['main']
        result = {
            'url': main_cfg['url'],
            'patterns': main_cfg.get('patterns', []),
            'period': main_cfg['period']
        }
        return result
