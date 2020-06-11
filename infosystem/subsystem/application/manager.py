from infosystem.common.subsystem import operation, manager


class Create(operation.Create):

    def do(self, session, **kwargs):
        self.entity = super().do(session, **kwargs)

        # Creating capabilities for new application
        routes = self.manager.api.routes.list()

        for route in routes:
            if not route.sysadmin:
                self.manager.api.capabilities.create(
                    application_id=self.entity.id, route_id=route.id)

        return self.entity


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
