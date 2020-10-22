from typing import List

from infosystem.common import exception, utils
from infosystem.common.input import RouteResource
from infosystem.common.subsystem import manager, operation
from infosystem.subsystem.capability.resource import Capability
from infosystem.subsystem.route.resource import Route


class CreateCapabilities(operation.Operation):
    """ Receive a list of resources for create capabilities
        resource -> ('url','method') """

    def _routes_without_capabilities(self, capabilities: List[Capability],
                                     routes: List[Route]) -> List[Route]:
        filtered_routes = []
        routes_capabilities_ids = [c.route_id for c in capabilities]
        for route in routes:
            if route.id not in routes_capabilities_ids:
                filtered_routes.append(route)

        return filtered_routes

    def _filter_routes(self, resources: List[RouteResource],
                       routes: List[Route]) -> List[str]:
        routes_ids = [route.id for route in routes
                      if (route.url, route.method) in resources]
        return routes_ids

    def _create_capability(self, application_id: str,
                           route_id: str) -> Capability:
        return Capability(utils.random_uuid(),
                          route_id=route_id,
                          application_id=application_id)

    def pre(self, session, id: str, **kwargs) -> bool:
        self.application_id = id
        resources = kwargs.get('resources', None)
        if not resources:
            raise exception.OperationBadRequest()

        routes = self.manager.api.routes.list(
            sysadmin=False, bypass=False, active=True)
        capabilities = self.manager.api.capabilities.list(
            application_id=self.application_id)
        routes_without_capabilities = \
            self._routes_without_capabilities(capabilities, routes)

        self.routes_ids = self._filter_routes(resources,
                                              routes_without_capabilities)

        return True
        # return self.driver.get(id, session=session) is not None

    def do(self, session, **kwargs) -> None:
        capabilities = [self._create_capability(self.application_id, route_id)
                        for route_id in self.routes_ids]

        session.bulk_save_objects(capabilities)


class Delete(operation.Delete):

    def pre(self, session, id, **kwargs):
        super().pre(session, id=id)
        policies = self.manager.api.policies.list(capability_id=id)
        if policies:
            message = 'You can\'t remove this capability because' + \
                ' there are policies associated'
            raise exception.BadRequest(message)
        return True


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create_capabilities = CreateCapabilities(self)
        self.delete = Delete(self)
