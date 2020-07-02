from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation


class CreatePolicies(operation.Operation):

    def pre(self, session, id: str, application_id: str, **kwargs):
        self.role_id = id
        self.application_id = application_id

        return self.manager.api.applications.get(id=application_id) \
            is not None and self.driver.get(id, session=session) is not None

    def _create_policy(self, role_id: str, capability_id: str) -> None:
        self.manager.api.policies.create(role_id=role_id,
                                         capability_id=capability_id)

    def do(self, session, **kwargs):
        capabilities = self.manager.api.capabilities.list(
            application_id=self.application_id)

        for capability in capabilities:
            self._create_policy(self.role_id, capability.id)


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create_policies = CreatePolicies(self)
