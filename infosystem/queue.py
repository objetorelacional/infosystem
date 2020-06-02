import flask
from typing import Any
from pika import BlockingConnection, PlainCredentials, \
                 ConnectionParameters, BasicProperties
from infosystem.celery import celery


class RabbitMQ:

    def __init__(self):
        self.url = flask.current_app.config['INFOSYSTEM_QUEUE_URL']
        self.port = flask.current_app.config['INFOSYSTEM_QUEUE_PORT']
        self.virtual_host = \
            flask.current_app.config['INFOSYSTEM_QUEUE_VIRTUAL_HOST']
        self.username = flask.current_app.config['INFOSYSTEM_QUEUE_USERNAME']
        self.password = flask.current_app.config['INFOSYSTEM_QUEUE_PASSWORD']
        credentials = PlainCredentials(self.username, self.password)
        self.params = ConnectionParameters(
            self.url, self.port, self.virtual_host, credentials)

    def connect(self):
        try:
            return BlockingConnection(self.params)
        except Exception:
            raise


class ProducerQueue:

    def __init__(self, exchange, exchange_type):
        rabbitMQ = RabbitMQ()
        self.connection = rabbitMQ.connect()
        self.exchange = exchange
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=exchange, exchange_type=exchange_type, durable=True)

    def publish(self, routing_key):
        body = ""
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=routing_key, body=body)
        self.close()

    def publish_with_body(self, routing_key, body):
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=routing_key, body=body)
        self.close()

    def publish_body_priority(self, routing_key, body, priority):
        properties = BasicProperties(priority=priority, type=self.exchange)
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=routing_key, body=body,
            properties=properties)
        self.close()

    def close(self):
        self.channel.close()
        self.connection.close()


@celery.task
def publish_body_priority(exchange: str,
                          priority: int,
                          body: Any,
                          routing_key: str = '',
                          type: str = 'topic') -> None:
    publish = ProducerQueue(exchange, type)
    publish.publish_body_priority(routing_key, body, priority)
