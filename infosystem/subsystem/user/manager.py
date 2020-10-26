import os
import hashlib

from sqlalchemy import or_, and_

from infosystem.common import exception
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation
from infosystem.subsystem.user.email import TypeEmail, send_email
from infosystem.subsystem.user.resource import User
from infosystem.subsystem.capability.resource import Capability
from infosystem.subsystem.domain.resource import Domain
from infosystem.subsystem.route.resource import Route
from infosystem.subsystem.grant.resource import Grant
from infosystem.subsystem.policy.resource import Policy
from infosystem.subsystem.role.resource import Role


class Create(operation.Create):

    def pre(self, session, **kwargs):
        self.role = self.manager.api.roles.get_role_by_name(
            role_name=Role.USER)
        return super().pre(session, **kwargs)

    def do(self, session, **kwargs):
        super().do(session)
        self.manager.api.grants.create(role_id=self.role.id,
                                       user_id=self.entity.id)
        return self.entity


class UpdatePassword(operation.Update):

    def _check_password(self, password, password_db):
        if not password:
            return password_db is None
        password_hash = self.manager.hash_password(password)
        return password_hash == password_db

    def pre(self, session, id, **kwargs):
        old_password = kwargs.pop('old_password', None)
        self.password = kwargs.pop('password', None)

        if not (id and self.password and old_password):
            raise exception.BadRequest()
        super().pre(session=session, id=id)

        if not self._check_password(old_password, self.entity.password):
            raise exception.BadRequest()
        return True

    def do(self, session, **kwargs):
        self.entity.password = self.manager.hash_password(self.password)
        self.entity = super().do(session)
        return self.entity


class Restore(operation.Operation):

    def pre(self, **kwargs):
        email = kwargs.get('email', None)
        domain_name = kwargs.get('domain_name', None)
        infosystem_reset_url = os.environ.get(
            'INFOSYSTEM_RESET_URL', 'http://objetorelacional.com.br/#/reset/')
        self.reset_url = kwargs.get('reset_url', infosystem_reset_url)

        if not (domain_name and email and self.reset_url):
            raise exception.OperationBadRequest()

        domains = self.manager.api.domains.list(name=domain_name)
        if not domains:
            raise exception.OperationBadRequest()

        self.domain = domains[0]

        users = self.manager.api.users.list(
            email=email, domain_id=self.domain.id)
        if not users:
            raise exception.OperationBadRequest()

        self.user = users[0]

        return True

    def do(self, session, **kwargs):
        self.manager.notify(
            id=self.user.id, type_email=TypeEmail.FORGOT_PASSWORD)
        # token = self.manager.api.tokens.create(user=self.user)
        # send_email(token.id, self.user, self.domain)


class Reset(operation.Update):

    def pre(self, session, id, **kwargs):
        self.password = kwargs.get('password', None)
        if not (id and self.password):
            raise exception.BadRequest()
        super().pre(session=session, id=id)
        return True

    def do(self, session, **kwargs):
        self.entity.password = self.manager.hash_password(self.password)
        self.entity = super().do(session)
        return self.entity


class Routes(operation.Operation):

    def do(self, session, user_id, **kwargs):
        routes = session.query(Route). \
            join(Capability). \
            join(Policy). \
            join(Grant, Policy.role_id == Grant.role_id). \
            join(User). \
            join(Domain,
                 and_(Domain.application_id == Capability.application_id,
                      Domain.id == User.domain_id)). \
            filter(or_(User.id == user_id, Route.bypass),
                   User.active, Domain.active, Grant.active,
                   Policy.active, Capability.active, Route.active). \
            distinct(). \
            all()

        return routes


class Authorization(operation.Operation):

    def do(self, session, user_id, route, **kwargs):
        has_capabilities = session.query(User.id). \
            join(Domain). \
            join(Grant). \
            join(Role). \
            join(Policy). \
            join(Capability,
                 and_(Capability.id == Policy.capability_id,
                      Capability.application_id == Domain.application_id,
                      Capability.route_id == route.id)). \
            filter(and_(User.id == user_id,
                        or_(not route.sysadmin, Role.name == 'sysadmin'),
                        User.active, Domain.active, Grant.active,
                        Policy.active, Capability.active)). \
            count()

        return has_capabilities > 0


class UploadPhoto(operation.Update):

    def pre(self, session, id, **kwargs):
        kwargs.pop('password', None)
        photo_id = kwargs.pop('photo_id', None)
        self.entity = self.manager.get(id=id)
        self.entity.photo_id = photo_id
        return self.entity.is_stable()

    def do(self, session, **kwargs):
        return super().do(session=session)


class DeletePhoto(operation.Update):

    def pre(self, session, id, **kwargs):
        kwargs.pop('password', None)
        self.entity = self.manager.get(id=id)
        self.photo_id = self.entity.photo_id
        self.entity.photo_id = None
        return self.entity.is_stable()

    def do(self, session, **kwargs):
        return super().do(session=session)

    def post(self):
        if self.photo_id:
            self.manager.api.images.delete(id=self.photo_id)


class Notify(operation.Operation):

    def _get_sysadmin(self):
        users = self.manager.list(name='sysadmin')
        user = users[0] if users else None
        return user

    def pre(self, session, id, type_email, **kwargs):
        self.user = self.manager.get(id=id)
        self.type_email = type_email
        if not self.user or not self.type_email:
            raise exception.BadRequest()
        return True

    def do(self, session, **kwargs):
        if self.type_email is TypeEmail.ACTIVATE_ACCOUNT:
            user_token = self._get_sysadmin()
        else:
            user_token = self.user

        self.token = self.manager.api.tokens.create(
            session=session, user=user_token)

        self.domain = self.manager.api.domains.get(id=self.user.domain_id)
        if not self.domain:
            raise exception.OperationBadRequest()

        send_email(self.type_email, self.token.id, self.user, self.domain)


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
        self.update_password = UpdatePassword(self)
        self.restore = Restore(self)
        self.reset = Reset(self)
        self.routes = Routes(self)
        self.upload_photo = UploadPhoto(self)
        self.delete_photo = DeletePhoto(self)
        self.notify = Notify(self)
        self.authorize = Authorization(self)

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
