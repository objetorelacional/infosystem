import uuid

from typing import Dict, List

from infosystem.common.subsystem import Subsystem
from infosystem.subsystem.role.resource import Role


class BootstrapRoles(object):

    def __init__(self, subsystems: Dict[str, Subsystem]):
        self.role_manager = subsystems['roles'].manager

    def execute(self):
        roles = self.role_manager.list()
        if not roles:
            default_roles = self._default_roles()
            roles = self.role_manager.create_roles(roles=default_roles)
        return roles

    def _get_role(self, name: str) -> Role:
        role = Role(id=uuid.uuid4().hex, name=name)
        return role

    def _default_roles(self) -> List[Role]:
        user = self._get_role(Role.USER)
        sysadmin = self._get_role(Role.SYSADMIN)
        admin = self._get_role(Role.ADMIN)

        return [user, sysadmin, admin]
