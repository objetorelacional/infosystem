import flask
from typing import List

from infosystem.common.subsystem import controller
from infosystem.common import exception
from infosystem.common.input import InputResource, InputResourceUtils


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super().__init__(manager, resource_wrap, collection_wrap)

    def _get_resources(self, input_resources) -> List[InputResource]:
        resources = []
        for input_resource in input_resources:
            endpoint = input_resource.get('endpoint')
            methods = input_resource.get('methods', [])
            resource = (endpoint, methods)
            resources.append(resource)

        return InputResourceUtils.parse_resources(resources)

    def create_policies(self, id: str):
        data = flask.request.get_json()
        try:
            resources = data.get('resources', [])
            data['resources'] = self._get_resources(resources)

            self.manager.create_policies(id=id, **data)

        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")
