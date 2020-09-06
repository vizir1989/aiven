from checker_kafka.kafka_consumer.consumer import CheckerConsumer
from checker_db.db_creator import db_create
from configuration.config import sentry_config, main_config, kafka_consumer_config
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

sentry_sdk.init(
    dsn=sentry_config()['dns'],
    integrations=[sentry_logging]
)

my_db = db_create('ps')
consumer = CheckerConsumer(my_db, main_config(), kafka_consumer_config())
consumer.start()
