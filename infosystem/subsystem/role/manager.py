from sqlalchemy import and_
from typing import List, Dict, Any
from infosystem.common import exception
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation
from infosystem.subsystem.capability.resource import Capability
from infosystem.subsystem.route.resource import Route


class CreatePolicies(operation.Operation):

    def pre(self, session, id: str, **kwargs):
        self.role_id = id
        self.application_id = kwargs.get('application_id', None)
        self.resources = kwargs.get('resources', None)

        if ((not (self.role_id and self.application_id)) or
                self.resources is None):
            raise exception.OperationBadRequest()

        return self.manager.api.applications.get(id=self.application_id) \
            is not None and self.driver.get(id, session=session) is not None

    def _create_policy(self, role_id: str, capability_id: str) -> None:
        self.manager.api.policies.create(role_id=role_id,
                                         capability_id=capability_id)

    def _filter_route(self, route, endpoint, exceptions) -> bool:
        is_in_exceptions = route.method in exceptions

        start_with = route.url.startswith("{}/".format(endpoint))
        match_endpoint = route.url == endpoint or start_with

        return not is_in_exceptions and match_endpoint

    def _filter_routes(self, resources: List[Dict[str, Any]],
                       routes: List[Route]) -> List[str]:
        routes_ids = []
        for resource in resources:
            endpoint = resource['endpoint']
            exceptions = resource.get('exceptions', [])

            routes_ids += [route.id for route in routes
                           if self._filter_route(route, endpoint, exceptions)]
        return routes_ids

    def do(self, session, **kwargs):
        routes = session.query(Route). \
            join(Capability). \
            filter(Capability.application_id == self.application_id,
                   ~Route.sysadmin, ~Route.bypass, Route.active). \
            all()

        routes_ids = self._filter_routes(self.resources, routes)

        capabilities = session.query(Capability.id). \
            filter(and_(Capability.application_id == self.application_id,
                        Capability.route_id.in_(routes_ids),
                        Capability.active)). \
            all()

        for capability in capabilities:
            self._create_policy(self.role_id, capability.id)


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create_policies = CreatePolicies(self)
