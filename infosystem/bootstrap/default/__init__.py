from typing import Dict, List

from infosystem.common.subsystem import Subsystem
from infosystem.common.input import RouteResource
from infosystem.subsystem.role.resource import Role
from infosystem.bootstrap.roles import BootstrapRoles
from infosystem.bootstrap.default.application import BootstrapApplication
from infosystem.bootstrap.default.domain import BootstrapDomain
from infosystem.bootstrap.default.user import BootstrapUser
from infosystem.bootstrap.default.policies import BootstrapPolicies


class BootstrapDefault(object):

    def __init__(self, subsystems: Dict[str, Subsystem]):
        self.bootstrap_roles = BootstrapRoles(subsystems)
        self.bootstrap_application = BootstrapApplication(subsystems)
        self.bootstrap_domain = BootstrapDomain(subsystems)
        self.bootstrap_user = BootstrapUser(subsystems)
        self.bootstrap_policies = BootstrapPolicies(subsystems)

    def execute(self, user_resources: List[RouteResource],
                sysadmin_resources: List[RouteResource],
                sysadmin_exclusive_resources: List[RouteResource]):
        roles = self.bootstrap_roles.execute()
        role_sysadmin = self._get_role_sysadmin(roles)

        application = self.bootstrap_application.execute()
        domain = self.bootstrap_domain.execute(application.id)
        self.bootstrap_user.execute(domain.id, role_sysadmin.id)
        self.bootstrap_policies.execute(application.id,
                                        role_sysadmin.id,
                                        user_resources,
                                        sysadmin_resources,
                                        sysadmin_exclusive_resources)

    def _get_role_sysadmin(self, roles: List[Role]) -> Role:
        role = next((role for role in roles if role.name == Role.SYSADMIN),
                    None)
        if not role:
            raise Exception()
        return role
