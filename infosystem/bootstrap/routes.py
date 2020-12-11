import uuid

from typing import Dict, List

from infosystem.common.subsystem import Subsystem
from infosystem.subsystem.route.resource import Route


class BootstrapRoutes(object):

    def __init__(self, subsystems: Dict[str, Subsystem]):
        self.route_manager = subsystems['routes'].manager
        self.subsystems_routes = self._get_routes_subsystems(subsystems)

    def _get_routes_subsystems(self,
                               subsystems: Dict[str, Subsystem]) -> List[Dict]:
        routes = [route for subsystem in subsystems.values()
                  for route in subsystem.router.routes]
        return routes

    def execute(self) -> List[Route]:
        routes_db = self._get_routes_db()
        # TODO inactivate old_routes
        (new_routes, old_routes) = self._get_diff_routes(
            self.subsystems_routes, routes_db)

        new_routes_db = self._get_create_routes(new_routes)
        self._save_routes(new_routes_db)

        return new_routes_db + routes_db

    def _get_routes_db(self) -> List[Route]:
        routes = self.route_manager.list()
        return routes

    def _get_diff_routes(self, routes_app: List[Dict], routes_db: List[Route]):
        new_routes, old_routes = [], []

        routes_db_tuples = [(route.url, route.method) for route in routes_db]
        routes_app_tuples = [(route['url'], route['method'])
                             for route in routes_app]

        for route in routes_app:
            if (route['url'], route['method']) not in routes_db_tuples:
                new_routes.append(route)

        for route in routes_db:
            if (route.url, route.method) not in routes_app_tuples:
                old_routes.append(route)

        return (new_routes, old_routes)

    def _get_create_routes(self, routes: List[Dict]) -> List[Route]:
        new_routes_db = []
        for route in routes:
            name = route['action']
            url = route['url']
            method = route['method']
            bypass = route.get('bypass', False)
            new_route = Route(id=uuid.uuid4().hex,
                              name=name,
                              url=url,
                              method=method,
                              bypass=bypass)
            new_routes_db.append(new_route)
        return new_routes_db

    def _save_routes(self, routes: List[Route]):
        if routes:
            self.route_manager.create_routes(routes=routes)
