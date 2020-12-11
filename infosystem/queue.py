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
        rabbitmq = RabbitMQ()
        self.connection = rabbitmq.connect()
        self.channel = self.connection.channel()

    def publish(self, exchange, routing_key, body, properties=None):
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=body,
                                   properties=properties)

    def _publish_entity(self, exchange, routing_key, body,
                        type, priority=None, headers=None):
        properties = BasicProperties(
            type=type, priority=priority, headers=headers)
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=body,
                                   properties=properties)

    def publish_full_entity(self, exchange, routing_key, body,
                            type, priority):
        headers = {'event_type': 'FULL_ENTITY'}
        self._publish_entity(exchange, routing_key, body,
                             type, priority, headers)

    def publish_request_entity(self, exchange, routing_key, body,
                               type, priority):
        headers = {'event_type': 'REQUEST_ENTITY'}
        self._publish_entity(exchange, routing_key, body,
                             type, priority, headers)

    def publish_partial_entity(self, exchange, routing_key, body,
                               type, priority, event_name):
        headers = {'event_type': 'PARTIAL_ENTITY', 'event_name': event_name}
        self._publish_entity(exchange, routing_key, body,
                             type, priority, headers)

    def run(self, fn, *args):
        fn(self, *args)
        self.close()

    def close(self):
        self.channel.close()
        self.connection.close()
