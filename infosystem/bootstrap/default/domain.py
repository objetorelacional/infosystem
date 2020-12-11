from typing import Dict

from infosystem.common import utils
from infosystem.common.subsystem import Subsystem
from infosystem.subsystem.domain.resource import Domain


class BootstrapDomain(object):

    def __init__(self, subsystems: Dict[str, Subsystem]):
        self.domain_manager = subsystems['domains'].manager

    def execute(self, application_id: str) -> Domain:
        domain = self._get_domain_default(application_id)
        return self._save_domain(domain)

    def _get_domain_default(self, application_default_id: str) -> Domain:
        return Domain(id=utils.random_uuid(),
                      application_id=application_default_id,
                      name=Domain.DEFAULT)

    def _save_domain(self, domain: Domain) -> Domain:
        data = domain.to_dict()
        if 'settings' in data.keys():
            data.pop('settings')
        data['addresses'] = []
        data['contacts'] = []
        return self.domain_manager.create(**data)
