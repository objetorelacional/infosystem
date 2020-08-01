from infosystem.common import exception
from infosystem.common.subsystem import operation, manager
from infosystem.subsystem.capability.resource import Capability
from infosystem.subsystem.policy.resource import Policy
from infosystem.subsystem.role.resource import Role


class CreateCapabilities(operation.Operation):

    def pre(self, session, id: str, **kwargs):
        self.application_id = id
        self.resources = kwargs.get('resources', None)
        if self.resources is None:
            raise exception.OperationBadRequest()

        return self.driver.get(id, session=session) is not None

    def _create_capability(self, application_id: str, route_id: str) -> None:
        self.manager.api.capabilities.create(application_id=application_id,
                                             route_id=route_id)

    def _filter_route(self, route, endpoint, exceptions):
        is_in_exceptions = route.method in exceptions

        start_with = route.url.startswith("{}/".format(endpoint))
        match_endpoint = route.url == endpoint or start_with

        return not is_in_exceptions and match_endpoint

    def _filter_routes(self, routes, endpoint, exceptions):
        return [route.id for route in routes
                if self._filter_route(route, endpoint, exceptions)]

    def do(self, session, **kwargs):
        routes = self.manager.api.routes.list(
            sysadmin=False, bypass=False, active=True)
        routes_ids = []

        for resource in self.resources:
            endpoint = resource['endpoint']
            exceptions = resource.get('exceptions', [])
            routes_ids += self._filter_routes(routes, endpoint, exceptions)

        for route_id in routes_ids:
            self._create_capability(self.application_id, route_id)


class GetRoles(operation.Operation):

    def pre(self, session, id, **kwargs):
        self.application_id = id
        return self.driver.get(id, session=session) is not None

    def do(self, session, **kwargs):
        roles = session.query(Role). \
            join(Policy). \
            join(Capability). \
            filter(Capability.application_id == self.application_id). \
            distinct()
        return roles


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create_capabilities = CreateCapabilities(self)
        self.get_roles = GetRoles(self)
