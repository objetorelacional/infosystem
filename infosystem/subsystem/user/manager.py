import os
import hashlib

from infosystem.common import exception
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation
from infosystem.subsystem.user.email import TypeEmail, send_email


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
        grants = self.manager.api.grants.list(user_id=user_id)
        grants_ids = [g.role_id for g in grants]
        roles = self.manager.api.roles.list()

        user_roles_id = [r.id for r in roles if r.id in grants_ids]

        # FIXME(fdoliveira) Try to send user_roles_id as paramater on query
        policies = self.manager.api.policies.list()
        policies_capabilitys_id = [
            p.capability_id for p in policies if p.role_id in user_roles_id]

        user = self.manager.api.users.list(id=user_id)[0]
        domain = self.manager.api.domains.get(id=user.domain_id)
        capabilities = self.manager.api.capabilities.list(
            application_id=domain.application_id)

        policy_capabilities = [
            c for c in capabilities if c.id in policies_capabilitys_id]

        # NOTE(samueldmq): if there is no policy for a capabiltiy,
        # then it's open! add it too!
        restricted_capabilities = [p.capability_id for p in policies]
        open_capabilities = [
            c for c in capabilities if c.id not in restricted_capabilities]

        user_routes = [self.manager.api.routes.get(id=c.route_id) for c in (
            policy_capabilities + open_capabilities)]

        bypass_routes = self.manager.api.routes.list(bypass=True)

        return list(set(user_routes).union(set(bypass_routes)))


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
        self.update_password = UpdatePassword(self)
        self.restore = Restore(self)
        self.reset = Reset(self)
        self.routes = Routes(self)
        self.upload_photo = UploadPhoto(self)
        self.delete_photo = DeletePhoto(self)
        self.notify = Notify(self)

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
