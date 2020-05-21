import json

import flask

from infosystem.common import exception
from infosystem.common.exception import BadRequest, InfoSystemException
from infosystem.common.subsystem import controller


class Controller(controller.Controller):

    def _get_name_in_args(self):
        name = flask.request.args.get('name', None)
        if not name:
            raise BadRequest()
        if name == 'default':
            e = InfoSystemException()
            e.status = 403
            e.message = 'Forbidden'
            raise e
        return name

    def _get_response_domain_name(self, entity):
        response = {
            "domain": {
                "id": entity.id,
                "name": entity.name
            }
        }
        return response

    def get_by_name(self):
        try:
            name = self._get_name_in_args()
            entity = self.manager.get_by_name(name=name)
            response = self._get_response_domain_name(entity)
            return flask.Response(response=json.dumps(response, default=str),
                                  status=200,
                                  mimetype="application/json")
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
