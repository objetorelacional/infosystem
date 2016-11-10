import flask

from infosystem.common.subsystem.controller import *
from infosystem.common.subsystem.driver import *
from infosystem.common.subsystem.manager import *
from infosystem.common.subsystem.router import *

import importlib
import os


def import_subsystems(system_dir, system_name):
    path = os.path.join(system_dir, 'subsystem')
    package = system_name + '.subsystem'
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    modules = [importlib.import_module(package + '.' + m) for m in dirs]
    return [m.subsystem for m in modules if hasattr(m, 'subsystem')]


class Subsystem(flask.Blueprint):

    def __init__(self, resource=None, router=None, controller=None, manager=None,
                 driver=None, individual_name=None, collection_name=None, operations=[]):
        individual_name = individual_name or resource.individual()
        collection_name = collection_name or resource.collection()

        super().__init__(collection_name, collection_name)

        driver = driver(resource) if driver else Driver(resource) if resource else None
        manager = manager(driver) if manager else Manager(driver)
        controller = controller(manager, individual_name, collection_name) if controller else Controller(manager, individual_name, collection_name)
        router = router(controller, collection_name, routes=operations) if router else Router(controller, collection_name, routes=operations)

        self.name = collection_name
        self.router = router
        self.manager = manager
        self.register_routes()

    def register_routes(self):
        for route in self.router.routes:
            self.add_url_rule(
                route['url'], view_func=route['callback'], methods=[route['method']])
