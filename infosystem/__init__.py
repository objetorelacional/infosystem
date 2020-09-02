import flask
import os

from infosystem import database
from infosystem import request
from infosystem import subsystem as subsystem_module
from infosystem import scheduler
from infosystem import celery


POLICYLESS_ROUTES = [
    ('POST', '/users/reset'),
    ('GET', '/users/<id>'),
    ('GET', '/users/routes')
]

SYSADMIN_RESOURCES = [
    ('POST', '/domains'),
    # ('PUT', '/domains/<id>'),
    ('DELETE', '/domains/<id>'),
    ('GET', '/domains'),

    ('POST', '/roles'),
    ('PUT', '/roles/<id>'),
    ('DELETE', '/roles/<id>'),

    ('POST', '/capabilities'),
    ('PUT', '/capabilities/<id>'),
    ('DELETE', '/capabilities/<id>'),

    ('POST', '/applications'),
    ('PUT', '/applications/<id>'),
    ('DELETE', '/applications/<id>'),
    ('GET', '/applications'),

    ('POST', '/policies'),
    ('PUT', '/policies/<id>'),
    ('DELETE', '/policies/<id>')
]


class System(flask.Flask):

    request_class = request.Request

    def __init__(self, *args, **kwargs):
        super().__init__(__name__, static_folder=None)

        self.configure()
        self.init_database()
        self.after_init_database()

        subsystem_list = subsystem_module.all + list(
            kwargs.values()) + list(args)

        self.subsystems = {s.name: s for s in subsystem_list}
        self.inject_dependencies()

        for subsystem in self.subsystems.values():
            self.register_blueprint(subsystem)

        # Add version in the root URL
        self.add_url_rule('/', view_func=self.version, methods=['GET'])

        self.scheduler = scheduler.Scheduler()
        self.schedule_jobs()

        self.bootstrap()

        self.before_request(
            request.RequestManager(self.subsystems).before_request)

    def configure(self):
        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    def init_database(self):
        database.db.init_app(self)
        with self.app_context():
            database.db.create_all()

    def after_init_database(self):
        pass

    def version(self):
        return '1.0.0'

    def schedule_jobs(self):
        pass

    def inject_dependencies(self):
        # api = lambda: None
        def api():
            None

        for name, subsystem in self.subsystems.items():
            setattr(api, name, subsystem.router.controller.manager)

        # Dependency injection
        for subsystem in self.subsystems.values():
            subsystem.router.controller.manager.api = api

    def register_all_routes(self, default_application_id, sysadmin_role_id):
        # Register all system routes and all non-admin
        # routes as capabilities in the default domain
        for subsystem in self.subsystems.values():
            for route in subsystem.router.routes:
                route_url = route['url']
                route_method = route['method']
                bypass_param = route.get('bypass', False)
                sysadmin_param = route.get('sysadmin', False)
                if (route_method, route_url) in SYSADMIN_RESOURCES:
                    sysadmin_param = True
                route_ref = self.subsystems['routes'].manager.create(
                    name=route['action'], url=route_url,
                    method=route['method'], bypass=bypass_param,
                    sysadmin=sysadmin_param)
                # TODO(samueldmq): duplicate the line above here and
                # see what breaks, it's probably the SQL
                # session management!
                if not (route_ref.sysadmin or route_ref.bypass):
                    cap_mng = self.subsystems['capabilities'].manager
                    capability = cap_mng.create(
                        application_id=default_application_id,
                        route_id=route_ref.id)
                    # TODO(fdoliveira) define why BYPASS atribute for URLs
                    # if (route_ref.method, route_ref.url) not in \
                    #        POLICYLESS_ROUTES:
                    self.subsystems['policies'].manager.create(
                        capability_id=capability.id,
                        role_id=sysadmin_role_id)

    def create_default_application(self):
        default_application = self.subsystems['applications'].manager.create(
            name='default', description='Application Default')
        return default_application

    def create_default_domain(self, default_application_id):
        # Create DEFAULT domain
        default_domain = self.subsystems['domains'].manager.create(
            name='default', application_id=default_application_id,
            addresses=[], contacts=[])

        # Create SYSDAMIN role
        sysadmin_role = self.subsystems['roles'].manager.create(
            name='sysadmin')

        # Create SYSADMIN user
        sysadmin_user = self.subsystems['users'].manager.create(
            domain_id=default_domain.id, name='sysadmin',
            email="sysadmin@example.com")
        self.subsystems['users'].manager.reset(
            id=sysadmin_user.id, password='123456')

        # Grant SYSADMIN role to SYSADMIN user
        self.subsystems['grants'].manager.create(
            user_id=sysadmin_user.id, role_id=sysadmin_role.id)

        self.register_all_routes(default_application_id, sysadmin_role.id)

    def bootstrap(self):
        """Bootstrap the system.

        - routes;
        - TODO(samueldmq): sysadmin;
        - default domain with admin and capabilities.

        """

        with self.app_context():
            if not self.subsystems['applications'].manager.list():
                default_application = self.create_default_application()
                if not self.subsystems['domains'].manager.list():
                    self.create_default_domain(default_application.id)

    def init_celery(self):
        celery.init_celery(self)
