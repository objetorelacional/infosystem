from infosystem.subsystem.application.resource import Application
from typing import List
from infosystem.common import exception
from infosystem.common.input import RouteResource, InputResource, \
    InputResourceUtils
from infosystem.common.subsystem import operation, manager
from infosystem.subsystem.capability.resource import Capability
from infosystem.subsystem.policy.resource import Policy
from infosystem.subsystem.role.resource import Role
from infosystem.subsystem.route.resource import Route


class Create(operation.Create):

    def pre(self, session, **kwargs) -> bool:
        self.exceptions = kwargs.pop('exceptions', [])

        return super().pre(session, **kwargs)

    def do(self, session, **kwargs):
        super().do(session)
        self.manager.create_user_capabilities_and_policies(id=self.entity.id,
                                                           session=session)
        if self.entity.name != Application.DEFAULT:
            self.manager.create_admin_capabilities_and_policies(
                id=self.entity.id, session=session, exceptions=self.exceptions)
        return self.entity


class CreateUserCapabilitiesAndPolicies(operation.Operation):

    def pre(self, session, id, **kwargs) -> bool:
        self.application_id = id
        self.user_resources = self.manager.bootstrap_resources.USER
        self.role_id = self.manager.api.roles.\
            get_role_by_name(role_name=Role.USER).id

        return True

    def do(self, session, **kwargs):
        self.resources = {'resources': self.user_resources}
        self.manager.api.capabilities.create_capabilities(
            id=self.application_id, **self.resources)

        self.resources['application_id'] = self.application_id
        self.manager.api.roles.create_policies(id=self.role_id,
                                               **self.resources)


class CreateAdminCapabilitiesAndPolicies(operation.Operation):

    def _map_routes(self, routes: List[Route]) -> List[RouteResource]:
        resources = [(route.url, route.method) for route in routes]
        return resources

    def _filter_resources(self, all_resources: List[RouteResource],
                          exceptions_resources: List[RouteResource],
                          sysadmin_exclusive_resources: List[RouteResource],
                          user_resources: List[RouteResource]) \
            -> List[RouteResource]:
        resources = InputResourceUtils.diff_resources(
            all_resources, sysadmin_exclusive_resources, user_resources,
            exceptions_resources)
        return resources

    def pre(self, session, id, exceptions: List[InputResource] = [], **kwargs):
        self.application_id = id
        exceptions_resources = InputResourceUtils.parse_resources(exceptions)

        routes = self.manager.api.routes.list(active=True)
        routes_resources = self._map_routes(routes)

        self.admin_role_id = self.manager.api.roles.\
            get_role_by_name(role_name=Role.ADMIN).id

        self.admin_resources = self._filter_resources(
            routes_resources, exceptions_resources,
            self.manager.bootstrap_resources.SYSADMIN_EXCLUSIVE,
            self.manager.bootstrap_resources.USER)
        return True

    def do(self, session, **kwargs):
        self.resources = {'resources': self.admin_resources}
        self.manager.api.capabilities.create_capabilities(
            id=self.application_id, **self.resources)

        self.resources['application_id'] = self.application_id
        self.manager.api.roles.create_policies(id=self.admin_role_id,
                                               **self.resources)


class CreateCapabilitiesWithExceptions(operation.Operation):

    def _filter_resources(self, routes: List[Route],
                          exceptions: List[RouteResource],
                          sysadmin_exclusive_resources: List[RouteResource],
                          user_resources: List[RouteResource]) \
            -> List[RouteResource]:
        all_resources = [(route.url, route.method) for route in routes]
        resources = InputResourceUtils.diff_resources(
            all_resources, sysadmin_exclusive_resources, user_resources,
            exceptions)
        return resources

    def pre(self, session, id: str, **kwargs):
        self.application_id = id
        exceptions = kwargs.get('exceptions', None)

        if not self.application_id or exceptions is None:
            raise exception.BadRequest()

        routes = self.manager.api.routes.list(active=True)
        exceptions_resources = InputResourceUtils.parse_resources(exceptions)
        self.resources = self.\
            _filter_resources(routes,
                              exceptions_resources,
                              self.manager.bootstrap_resoures.
                              SYSADMIN_EXCLUSIVE,
                              self.manager.bootstrap_resources.USER)

        return self.driver.get(id, session=session) is not None

    def do(self, session, **kwargs):
        data = {'resources', self.resources}
        self.manager.api.capabilities.\
            create_capabilities(id=self.application_id, **data)


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
        self.create = Create(self)
        self.create_user_capabilities_and_policies = \
            CreateUserCapabilitiesAndPolicies(self)
        self.create_admin_capabilities_and_policies = \
            CreateAdminCapabilitiesAndPolicies(self)
        self.get_roles = GetRoles(self)
