from infosystem.common.subsystem import operation, manager


class Create(operation.Create):

    def do(self, session, **kwargs):
        self.entity = super().do(session, **kwargs)

        # Creating capabilities for new application
        # routes = self.manager.api.routes.list()

        # for route in routes:
        #     if not route.sysadmin:
        #         self.manager.api.capabilities.create(
        #             application_id=self.entity.id, route_id=route.id)

        return self.entity


class CreateCapabilities(operation.Operation):

    def pre(self, session, id: str, **kwargs):
        self.application_id = id
        return self.driver.get(id, session=session) is not None

    def _create_capability(self, application_id: str, route_id: str) -> None:
        self.manager.api.capabilities.create(application_id=application_id,
                                             route_id=route_id)

    def do(self, session, **kwargs):
        routes = self.manager.api.routes.list(sysadmin=False)

        for route in routes:
            self._create_capability(self.application_id, route.id)


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
        self.create_capabilities = CreateCapabilities(self)
