import os
import hashlib
import flask

from sparkpost import SparkPost
from infosystem.common import exception
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation

_HTML_EMAIL_TEMPLATE = """
    <div style="width: 100%; text-align: center">
        <h1>{app_name}</h1>
        <h2>CONFIRMAR E CRIAR SENHA</h2>
    </div>

    <p>Você acaba de ser cadastrado no portal da
        {app_name}.</p>
    <p>Para ter acesso ao sistema você deve clicar no link abaixo
        para confirmar esse email e criar uma senha.</p>

    <div style="width: 100%; text-align: center">
        <a href="{reset_url}">Clique aqui para CONFIRMAR o
            email e CRIAR uma senha.</a>
    </div>
"""


def send_email(token_id, user, domain):
    try:
        sparkpost = SparkPost()

        default_app_name = "INFOSYSTEM"
        default_email_use_sandbox = False
        default_reset_url = 'http://objetorelacional.com.br/#/reset'
        default_noreply_email = 'noreply@objetorelacional.com.br'
        default_email_subject = 'INFOSYSTEM - CONFIRMAR email e CRIAR senha'

        infosystem_app_name = os.environ.get(
            'INFOSYSTEM_APP_NAME', default_app_name)
        infosystem_reset_url = os.environ.get(
            'INFOSYSTEM_RESET_URL', default_reset_url)
        infosystem_noreply_email = os.environ.get(
            'INFOSYSTEM_NOREPLY_EMAIL', default_noreply_email)
        infosystem_email_subject = os.environ.get(
            'INFOSYSTEM_EMAIL_SUBJECT', default_email_subject)
        infosystem_email_use_sandbox = os.environ.get(
            'INFOSYSTEM_EMAIL_USE_SANDBOX',
            default_email_use_sandbox) == 'True'

        url = infosystem_reset_url + '/' + token_id + '/' + domain.name

        sparkpost.transmissions.send(
            use_sandbox=infosystem_email_use_sandbox,
            recipients=[user.email],
            html=_HTML_EMAIL_TEMPLATE.format(
                app_name=infosystem_app_name, reset_url=url),
            from_email=infosystem_noreply_email,
            subject=infosystem_email_subject
        )
    except Exception:
        # TODO(fdoliveira): do something here!
        pass


class Create(operation.Create):

    def do(self, session, **kwargs):
        self.entity = super().do(session, **kwargs)

        self.token = self.manager.api.tokens.create(
            session=session, user=self.entity)

        self.domain = self.manager.api.domains.get(id=self.entity.domain_id)
        if not self.domain:
            raise exception.OperationBadRequest()

        return self.entity

    # def post(self):
        # send_reset_password_email(self.token.id, self.entity, _RESET_URL)
        # send_email(self.token.id, self.entity, self.domain)


class Update(operation.Update):

    def do(self, session, **kwargs):
        password = kwargs.get('password', None)
        if password:
            kwargs['password'] = hashlib.sha256(
                password.encode('utf-8')).hexdigest()

        self.entity = super().do(session, **kwargs)

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
        token = self.manager.api.tokens.create(user=self.user)
        send_email(token.id, self.user, self.domain)


class Reset(operation.Operation):

    def pre(self, **kwargs):
        self.token = flask.request.headers.get('token')
        self.password = kwargs.get('password')

        if not (self.token and self.password):
            raise exception.OperationBadRequest()
        return True

    def do(self, session, **kwargs):
        token = self.manager.api.tokens.get(id=self.token)
        self.manager.update(id=token.user_id, password=self.password)

    def post(self):
        self.manager.api.tokens.delete(id=self.token)


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


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
        self.update = Update(self)
        self.restore = Restore(self)
        self.reset = Reset(self)
        self.routes = Routes(self)
        self.upload_photo = UploadPhoto(self)
        self.delete_photo = DeletePhoto(self)
