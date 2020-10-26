from typing import List

from infosystem.common.subsystem import operation, manager
from infosystem.subsystem.route.resource import Route


class CreateRoutes(operation.Operation):

    def pre(self, routes: List[Route], session, **kwargs) -> bool:
        self.routes = routes
        return True

    def do(self, session, **kwargs) -> List[Route]:
        session.bulk_save_objects(self.routes)
        return self.routes


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create_routes = CreateRoutes(self)
