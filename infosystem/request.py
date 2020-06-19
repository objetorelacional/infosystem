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

        if route.sysadmin:
            # TODO(samueldmq): implement sysadmin logic
            return

        if route.bypass:
            # lookup the domain specified as domain_name in the request body
            data = flask.request.get_json()
            if data and data.get('domain_name'):
                domains = self.subsystems['domains'].manager.list(
                    name=data['domain_name'])
                if domains:
                    application_id = domains[0].application_id

                    if not self.check_capability(route.id, application_id):
                        return flask.Response(response=None, status=404)
                else:
                    return flask.Response(response=None, status=400)
            # TODO(samueldmq): THIS SHOULD BE RE-ENABLED,
            # DISABLED FOR NOW FOR /FOTOS
            # else:
            #     return flask.Response(response=None, status=400)
        else:
            token_id = flask.request.token

            if token_id:
                try:
                    token = self.subsystems['tokens'].manager.get(id=token_id)
                except exception.NotFound:
                    return flask.Response(response=None, status=401)

                user = self.subsystems['users'].manager.list(
                    id=token.user_id)[0]
                domain = self.subsystems['domains'].manager.get(
                    id=user.domain_id)

                # TODO Checar domain
                # 1 - sem domain seta o default obs: apenas o sysadmin pode
                #       gravar no default
                # 2 checar se o domain enviado corresponde ao do token

                if not self.check_capability(route.id, domain.application_id):
                    return flask.Response(response=None, status=404)

                # Now check the user grants
                grants = self.subsystems['grants'].manager.list(
                    user_id=user.id)
                user_role_ids = [g.role_id for g in grants]

                # TODO(samueldmq): sysadmin won't provide a domain,
                # so capabilities will be empty
                # treat this case here once we support sysadmin
                capability = self.subsystems['capabilities'].manager.list(
                    route_id=route.id, application_id=domain.application_id)[0]

                policies = self.subsystems['policies'].manager.list(
                    capability_id=capability.id)

                # open capability
                if not policies:
                    return

                policy_role_ids = [p.role_id for p in policies]

                intersection = set(user_role_ids).intersection(policy_role_ids)
                if not intersection:
                    return flask.Response(response=None, status=401)
            else:
                return flask.Response(response=None, status=401)

    def check_capability(self, route_id, application_id):
        capabilities = self.subsystems['capabilities'].manager.list(
            route_id=route_id, application_id=application_id)
        return capabilities
