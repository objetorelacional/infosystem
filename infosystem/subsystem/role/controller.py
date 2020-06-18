import flask
from typing import Optional

from infosystem.common.subsystem import controller
from infosystem.common import exception


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super().__init__(manager, resource_wrap, collection_wrap)

    def _get_application_id_from_request(self) -> Optional[str]:
        data = flask.request.get_json()
        return data.get('application_id', None)

    def create_policies(self, id: str):
        try:
            application_id = self._get_application_id_from_request()
            if not application_id:
                raise exception.BadRequest()

            self.manager.create_policies(id=id,
                                         application_id=application_id)

        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")
