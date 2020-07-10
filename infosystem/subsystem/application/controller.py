import flask

from infosystem.common import exception, utils
from infosystem.common.subsystem import controller


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super().__init__(manager, resource_wrap, collection_wrap)

    def create_capabilities(self, id: str):
        data = flask.request.get_json()
        try:

            self.manager.create_capabilities(id=id, **data)

        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")

    def get_roles(self, id: str):
        try:
            roles = self.manager.get_roles(id=id)
            response = {"roles": [role.to_dict() for role in roles]}

        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")
