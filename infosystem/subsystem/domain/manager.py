from infosystem.common.exception import NotFound
from infosystem.common.subsystem import operation, manager


class GetByName(operation.Operation):

    def pre(self, session, name, **kwargs):
        self.name = name
        return True

    def do(self, session, **kwargs):
        entities = self.manager.list(name=self.name)
        if not entities:
            raise NotFound()
        entity = entities[0]
        return entity


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.get_by_name = GetByName(self)
