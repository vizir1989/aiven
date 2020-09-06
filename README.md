# Checker

## What is this?

A system that monitors website availability over the
network, produces metrics about this and passes these events through an
Kafka instance into an PostgreSQL database.

For this, Kafka producer which periodically checks the target
websites and sends the check results to a Kafka topic, and a Kafka consumer
storing the data to an PostgreSQL database.

The website checker perform the checks periodically and collect the
HTTP response time, error code returned, as well as optionally checking the
returned page contents for a regexp pattern that is expected to be found on the
page.

## How to use

### docker

```
    docker build .
    docker-compose up
```

### bash

Creating task
```
celery -A checker.checker_producer beat
```

Creating worker
```
celery -A checker.checker_producer worker
```

Creating consumer
```
export PYTHONPATH=<current path>
python checker/chekcer_consumer.py
```

## Configuration file

There is configuration/config.yaml - configuration file, where you can configure application
Main section contain information about target url, regex and period
```
main:
  url: 'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml'
  patterns:
    - 'test'
  period: 10
```

## Library

### Celery + Redis
I use celery + redis for periodic tasks

### Kafka
I use kafka for produce and consume message about webpage

### PostgreSQL
I use Postgres for saving information about webpage

### Sentry
I use sentry for managment logs and collect information about problem

### Tox
I use tox for testing application

## What can be improved

* Add MongoDB
* Use async instead of sync library
* Add pytest-postgresql and pytest-kafka for testing
* Add Flower for celery monitoring
* Add health checker (may be add grafanalib)