from celery import Celery
from parser.parser import parse
from checker_kafka.kafka_producer.producer import CheckerProducer
from configuration.config import celery_config, main_config, sentry_config
from typing import List

import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=sentry_config()['dns'],
    integrations=[sentry_logging]
)

app = Celery(**celery_config())


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    logging.info('setup periodic tasks')
    cfg = main_config()
    period = cfg['period']
    sender.add_periodic_task(period, checker.s(cfg['url'], cfg['patterns']), name='checker')


@app.task
def checker(url: str, patterns: List[str]):
    logging.info('start checker')
    status_code, elapsed, results = parse(url, patterns)
    logging.info(
        f'checker results for {url} ({patterns}) status_code: {status_code}, elapsed: {elapsed}, results: {results}.'.format(
            url=url, patterns=patterns, status_code=status_code, elapsed=elapsed, results=results))
    producer = CheckerProducer()
    logging.info('send message')
    producer.send_message(status_code, elapsed, results)
    logging.info('message have been sent')
