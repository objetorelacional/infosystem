import flask
from typing import Optional

from infosystem.common.subsystem import controller
from infosystem.common import exception


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super().__init__(manager, resource_wrap, collection_wrap)

    def create_policies(self, id: str):
        data = flask.request.get_json()
        try:

            self.manager.create_policies(id=id, **data)

        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")
