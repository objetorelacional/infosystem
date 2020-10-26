from typing import Dict, List

from infosystem.common.input import RouteResource, InputResourceUtils
from infosystem.common.subsystem import Subsystem


class BootstrapPolicies(object):

    def __init__(self, subsystems: Dict[str, Subsystem]):
        self.capability_manager = subsystems['capabilities'].manager
        self.role_manager = subsystems['roles'].manager

    def execute(self, application_id: str,
                role_id: str,
                user_resources: List[RouteResource],
                sysadmin_resources: List[RouteResource],
                sysadmin_exclusive_resources: List[RouteResource]):
        capabilities_resources = InputResourceUtils. \
            join_resources(user_resources,
                           sysadmin_resources,
                           sysadmin_exclusive_resources)
        policies_resources = InputResourceUtils. \
            join_resources(sysadmin_resources,
                           sysadmin_exclusive_resources)

        self._save_capabilities(application_id, capabilities_resources)
        self._save_policies(application_id, role_id, policies_resources)

    def _save_capabilities(self, application_id: str,
                           resources: List[RouteResource]):
        data = {'resources': resources}
        self.capability_manager.create_capabilities(id=application_id,
                                                    **data)

    def _save_policies(self, application_id: str,
                       role_id: str,
                       resources: List[RouteResource]) -> None:
        data = {'resources': resources, 'application_id': application_id}
        self.role_manager.create_policies(id=role_id, **data)
