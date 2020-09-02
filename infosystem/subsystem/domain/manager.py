from infosystem.common import exception
from infosystem.subsystem.domain import tasks
from infosystem.common.subsystem import operation, manager


class DomainByName(operation.Operation):

    def pre(self, session, name, **kwargs):
        self.name = name
        return True

    def do(self, session, **kwargs):
        entities = self.manager.list(name=self.name)
        if not entities:
            raise exception.NotFound()
        entity = entities[0]
        return entity


class UploadLogo(operation.Update):

    def pre(self, session, id, token, file, **kwargs):
        self.file = file
        self.token = token

        return super().pre(session, id, **kwargs)

    def do(self, session, **kwargs):
        kwargs = {}
        kwargs['domain_id'] = self.entity.id
        kwargs['user_id'] = self.token.user_id
        kwargs['type_image'] = 'DomainLogo'

        image = self.manager.api.images.create(file=self.file, **kwargs)

        self.entity.logo_id = image.id

        return super().do(session=session)


class RemoveLogo(operation.Update):

    def do(self, session, **kwargs):
        logo_id = self.entity.logo_id
        self.entity.logo_id = None
        entity = super().do(session=session)
        if logo_id and entity is not None:
            self.manager.api.images.delete(id=logo_id)

        return


class Register(operation.Create):

    def pre(self, session, username, email, password,
            domain_name, domain_display_name, application_name):
        self.username = username
        self.email = email
        self.password = password
        self.domain_name = domain_name
        self.domain_display_name = domain_display_name
        self.application_name = application_name

        if not (username and email and password and
                domain_name and application_name):
            raise exception.BadRequest('ERROR! Not enogth data')

        applications = \
            self.manager.api.applications.list(name=application_name)
        if not applications:
            raise exception.BadRequest('ERROR! Application name not found.')
        self.application = applications[0]

        return True

    def do(self, session, **kwargs):
        domain = self.manager.api.domains.create(
            application_id=self.application.id, name=self.domain_name,
            display_name=self.domain_display_name, addresses=[], contacts=[],
            active=False)
        self.user = self.manager.api.users.create(
            name=self.username, email=self.email,
            domain_id=domain.id, active=False)
        self.manager.api.users.reset(id=self.user.id, password=self.password)

        return True

    def post(self):
        # The notification don't be part of transaction must be on post
        tasks.send_email.delay(self.user.id)


class Activate(operation.Create):

    def pre(self, session, token_id, domain_id, user_admin_id):
        if not (user_admin_id or domain_id):
            raise exception.BadRequest(
                'ERROR! Not enough data to Activate Domain')

        self.token_id = token_id
        self.domain_id = domain_id
        self.user_admin_id = user_admin_id

        roles = self.manager.api.roles.list(name='Admin')
        if not roles:
            raise exception.BadRequest('ERROR! Role Admin not found')
        self.role_admin = roles[0]

        return True

    def do(self, session, **kwargs):
        self.manager.api.domains.update(id=self.domain_id, active=True)
        self.manager.api.users.update(id=self.user_admin_id, active=True)
        self.manager.api.grants.create(user_id=self.user_admin_id,
                                       role_id=self.role_admin.id)
        self.manager.api.tokens.delete(id=self.token_id)

        return True


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.domain_by_name = DomainByName(self)
        self.upload_logo = UploadLogo(self)
        self.remove_logo = RemoveLogo(self)
        self.register = Register(self)
        self.activate = Activate(self)
