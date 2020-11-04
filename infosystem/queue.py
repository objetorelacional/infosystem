import flask
from pika import BlockingConnection, PlainCredentials, \
    ConnectionParameters, BasicProperties


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

    def __init__(self):
        rabbitMQ = RabbitMQ()
        self.connection = rabbitMQ.connect()
        self.channel = self.connection.channel()

    def publish(self, exchange, routing_key, body, properties=None):
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=body,
                                   properties=properties)

    def publish_with_priority(self, exchange, routing_key, body,
                              type, priority):
        properties = BasicProperties(type=type, priority=priority)
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=body,
                                   properties=properties)

    def run(self, fn, *args):
        fn(self, *args)
        self.close()

    def close(self):
        self.channel.close()
        self.connection.close()
