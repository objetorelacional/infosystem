from typing import List, Optional
from infosystem.common import exception, utils
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation
from infosystem.subsystem.role.resource import Role
from infosystem.subsystem.policy.resource import Policy


class CreatePolicies(operation.Operation):

    def _filter_capabilities(self, routes, capabilities, policies, resources):
        policies_capabilities_ids = [policy.capability_id
                                     for policy in policies]
        capabilities = [c for c in capabilities
                        if c.id not in policies_capabilities_ids]
        routes_ids = [route.id for route in routes
                      if (route.url, route.method) in resources]

        filtered_capabilities = [capability for capability in capabilities
                                 if capability.route_id in routes_ids]
        return filtered_capabilities

    def _create_policy(self, role_id: str, capability_id: str) -> Policy:
        return Policy(id=utils.random_uuid(),
                      role_id=role_id,
                      capability_id=capability_id)

    def pre(self, session, id: str, **kwargs) -> bool:
        self.role_id = id
        self.application_id = kwargs.get('application_id', None)
        resources = kwargs.get('resources', None)

        if ((not (self.role_id and self.application_id)) or resources is None):
            raise exception.OperationBadRequest()

        try:
            self.manager.api.applications.get(id=self.application_id)
        except exception.NotFound:
            raise exception.BadRequest('Invalid application')

        routes = self.manager.api.routes.list(
            sysadmin=False, bypass=False, active=True)
        capabilities = self.manager.api.capabilities.list(
            application_id=self.application_id)
        policies = self.manager.api.policies.list(role_id=self.role_id)
        self.capabilities = self._filter_capabilities(routes,
                                                      capabilities,
                                                      policies,
                                                      resources)
        return self.driver.get(id, session) is not None

    def do(self, session, **kwargs) -> None:
        policies = [self._create_policy(self.role_id, capability.id)
                    for capability in self.capabilities]
        session.bulk_save_objects(policies)


class CreateRoles(operation.Operation):

    def pre(self, roles: List[Role], session, **kwargs) -> bool:
        self.roles = roles
        return True

    def do(self, session, **kwargs) -> List[Role]:
        session.bulk_save_objects(self.roles)
        return self.roles


class GetRoleByName(operation.Operation):

    def pre(self, role_name: str, session, **kwargs) -> bool:
        self.roles = self.manager.list(name=role_name)
        return self.roles is not []

    def do(self, session, **kwargs) -> Optional[Role]:
        return self.roles[0]


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create_policies = CreatePolicies(self)
        self.create_roles = CreateRoles(self)
        self.get_role_by_name = GetRoleByName(self)
