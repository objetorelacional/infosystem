import flask
import json

from infosystem.common import utils
from infosystem.common.subsystem import controller
from infosystem.common import exception


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super(Controller, self).__init__(
            manager, resource_wrap, collection_wrap)

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

    def restore(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            self.manager.restore(**data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=200,
                              mimetype="application/json")

    def reset(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            self.manager.reset(**data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=200,
                              mimetype="application/json")

    def routes(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        token = self.manager.api.tokens.get(
            id=flask.request.headers.get('token'))
        try:
            routes = self.manager.routes(user_id=token.user_id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {"routes": [route.to_dict() for route in routes]}

        return flask.Response(response=json.dumps(response, default=str),
                              status=200,
                              mimetype="application/json")

    def upload_photo(self, id, **kwargs):
        try:
            file = flask.request.files.get('file', None)
            if not file:
                raise exception.BadRequest()

            token = self.get_token(self.get_token_id())
            domain_id = self.get_domain_id_from_token(token)
            user_id = token.user_id

            if not (domain_id and user_id):
                raise exception.BadRequest()

            kwargs['domain_id'] = domain_id
            kwargs['user_id'] = user_id
            kwargs['type_image'] = 'UserPhoto'
            image = self.manager.api.images.create(file=file, **kwargs)

            kwargs.pop('type_image')
            kwargs['photo_id'] = image.id
            self.manager.upload_photo(id=id, **kwargs)

            response = {'image': image.to_dict()}
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype="application/json")

    def delete_photo(self, id):
        try:
            self.manager.delete_photo(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")
