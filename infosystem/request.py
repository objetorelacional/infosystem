import flask
import uuid

from infosystem.common import exception


class Request(flask.Request):

    # TODO(samueldmq): find a better place to put this utility method
    def _check_uuid4(self, uuid_str):
        if len(uuid_str) != 32:
            return False
        try:
            return uuid.UUID(uuid_str, version=4)
        except ValueError:
            return False

    @property
    def method(self):
        return self.environ['REQUEST_METHOD']

    @property
    def url(self):
        path_info = flask.request.environ['PATH_INFO'].rstrip('/')
        path_bits = [
            '<id>' if self._check_uuid4(i) else i for i in path_info.split('/')
        ]

        if path_bits.count('<id>') > 1:
            pos = 0
            qty_id = 1
            for bit in path_bits:
                if bit == '<id>':
                    path_bits[pos] = '<id' + str(qty_id) + '>'
                    qty_id += 1
                pos += 1
        return '/'.join(path_bits)

    @property
    def token(self):
        return flask.request.headers.get('token')


class RequestManager(object):

    def __init__(self, subsystems):
        self.subsystems = subsystems

    def before_request(self):
        if flask.request.method == 'OPTIONS':
            return

        # Short-circuit if accessing the root URL,
        # which will just return the version
        # TODO(samueldmq): Do we need to create a subsystem just for this ?
        if not flask.request.url:
            return

        routes = self.subsystems['routes'].manager.list(
            url=flask.request.url, method=flask.request.method)
        if not routes:
            return flask.Response(response=None, status=404)
        route = routes[0]

        if not route.active:
            return flask.Response(response=None, status=410)

        if route.bypass:
            return

        token_id = flask.request.token

        if not token_id:
            return flask.Response(response=None, status=401)

        try:
            token = self.subsystems['tokens'].manager.get(id=token_id)
        except exception.NotFound:
            return flask.Response(response=None, status=401)

        can_access = self.subsystems['users'].manager.authorize(
            user_id=token.user_id, route=route)

        if not can_access:
            return flask.Response(response=None, status=403)
        return
