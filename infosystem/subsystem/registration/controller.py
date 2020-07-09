import flask
from infosystem.common.subsystem import controller
from infosystem.common import exception
from infosystem.subsystem.user.email import TypeEmail


class Controller(controller.Controller):

    def _get_token_id(self):
        return flask.request.headers.get('token')

    def _get_application_by_name(self, name):
        applications = self.manager.api.applications.list(name=name)
        if not applications:
            raise exception.BadRequest()
        return applications[0]

    def _get_register_data(self):
        data = flask.request.get_json()

        username = data.get('username', 'admin')
        email = data.get('email', None)
        password = data.get('password', None)
        domain_name = data.get('domain', None)
        application_name = data.get('application', None)

        if not (username and email and password and domain_name and
                application_name):
            raise exception.BadRequest()

        return (username, email, password, domain_name, application_name)

    def register(self):

        try:
            (username, email, password, domain_name, application_name) = \
                self._get_register_data()

            application = self._get_application_by_name(application_name)

            domain = self.manager.api.domains.create(
                name=domain_name, application_id=application.id, active=False)
            user = self.manager.api.users.create(
                name=username, email=email, domain_id=domain.id, active=False)
            self.manager.api.users.reset(id=user.id, password=password)
            self.manager.api.users.notify(
                id=user.id, type_email=TypeEmail.ACTIVATE_ACCOUNT)

        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")

    def _get_activate_data(self):
        data = flask.request.get_json()

        user_id = data.get('user_id', None)
        domain_id = data.get('domain_id', None)

        if not (user_id and domain_id):
            raise exception.BadRequest()

        return (user_id, domain_id)

    def _get_role_admin(self):
        roles = self.manager.api.roles.list(name='Admin')
        if not roles:
            raise exception.BadRequest()
        return roles[0]

    def activate(self):
        try:
            (user_id, domain_id) = self._get_activate_data()

            domain = self.manager.api.domains.get(id=domain_id)
            user = self.manager.api.users.get(id=user_id)

            if not (domain and user):
                raise exception.BadRequest()
            role_admin = self._get_role_admin()

            self.manager.api.domains.update(id=domain.id, active=True)
            self.manager.api.users.update(id=user.id, active=True)
            self.manager.api.grants.create(user_id=user.id,
                                           role_id=role_admin.id)
            self.manager.api.tokens.delete(id=self._get_token_id())
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")
