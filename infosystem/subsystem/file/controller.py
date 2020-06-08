import json

import flask

from infosystem.common import exception
from infosystem.common.exception import BadRequest
from infosystem.common.subsystem import controller

# TODO(samueldmq): take a better look at this, it is completely different as it
# is not dealing with JSON content


def get_bad_request(cause=None):
    bad_request = BadRequest()
    bad_request.message = cause if not None else bad_request.message

    return flask.Response(response=bad_request.message,
                          status=bad_request.status)


class Controller(controller.Controller):

    def get_token_id(self):
        return flask.request.headers.get('token')

    def get_token(self, token_id):
        return self.manager.api.tokens.get(id=token_id)

    def get_domain(self, domain_id):
        return self.manager.api.domains.get(id=domain_id)

    def get_domain_id_from_token(self, token):
        user = self.manager.api.users.get(id=token.user_id)
        return user.domain_id

    def get_domain_id(self):
        token = self.get_token(self.get_token_id())
        domain_id = self.get_domain_id_from_token(token)
        return domain_id

    def create(self, **kwargs):
        # TODO(samueldmq): the file should be extracted here.
        # the todo above would be resolved too with this!
        try:
            file = flask.request.files.get('file', None)
            if not file:
                return get_bad_request('file é obrigatório')

            token = self.get_token(self.get_token_id())
            domain_id = self.get_domain_id_from_token(token)
            if not domain_id:
                return get_bad_request(
                    'Não foi possível determinar o domain_id')

            user_id = token.user_id
            if not user_id:
                return get_bad_request(
                    'Não foi possível determinar o user')

            kwargs['domain_id'] = domain_id
            kwargs['user_id'] = user_id
            entity = self.manager.create(file=file, **kwargs)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=json.dumps(response, default=str),
                              status=201,
                              mimetype="application/json")

    def get(self, id):
        return self.manager.get(id=id)
