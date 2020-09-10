from typing import List

from infosystem.common.subsystem import Subsystem
from infosystem.common.input import InputResource, InputResourceUtils


class System(object):

    def __init__(self, name: str,
                 subsystems: List[Subsystem],
                 user_resources: List[InputResource] = [],
                 sysadmin_resources: List[InputResource] = [],
                 sysadmin_exclusive_resources: List[InputResource] = []):
        self.name = name
        self.subsystems = subsystems

        parse_resources = InputResourceUtils.parse_resources
        self.user_resources = parse_resources(user_resources)
        self.sysadmin_exclusive_resources = \
            parse_resources(sysadmin_exclusive_resources)
        self.sysadmin_resources = parse_resources(sysadmin_resources)
        self.sysadmin_resources = InputResourceUtils.\
            join_resources(self.sysadmin_resources,
                           self.sysadmin_exclusive_resources)
