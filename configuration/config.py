import yaml
import os
from typing import Dict, Tuple

script_dir = os.path.dirname(__file__) + '/'


def kafka_producer_config() -> Tuple[str, Dict]:
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
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        celery_cfg = cfg['celery']
        result = {
            'main': celery_cfg['main'],
            'broker': celery_cfg['broker_url'],
            'backend': celery_cfg.get('backend_url', None),
        }
        return result


def db_config() -> Dict:
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
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        sentry_cfg = cfg['sentry']
        result = {
            'dns': sentry_cfg['dns']
        }
        return result


def main_config() -> Dict:
    with open(script_dir + 'config.yml', 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        main_cfg = cfg['main']
        result = {
            'url': main_cfg['url'],
            'patterns': main_cfg.get('patterns', [])
        }
        return result
