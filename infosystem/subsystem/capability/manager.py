from infosystem.common.subsystem import operation, manager
from infosystem.common import exception


class Delete(operation.Delete):

    def pre(self, session, id, **kwargs):
        super().pre(session, id=id)
        policies = self.manager.api.policies.list(capability_id=id)
        if policies:
            message = 'You can\'t remove this capability because' + \
                ' there are policies associated'
            raise exception.BadRequest(message)


class Manager(manager.Manager):
    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.delete = Delete(self)
