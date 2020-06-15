from infosystem.common import exception
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation


class CreateAdmin(operation.Operation):

    def pre(self, **kwargs):

        applications = self.manager.api.applications.list(name='default')
        if not applications:
            raise exception.OperationBadRequest()
        self.application_id = applications[0].id

        if (self.application_id is None):
            raise exception.OperationBadRequest()

        if self.manager.api.roles.list(name='admin'):
            raise exception.OperationBadRequest()

        return True

    def do(self, session, **kwargs):
        self.entity = self.manager.api.roles.create(name='admin')

        routes = self.manager.api.routes.list()

        for route in routes:
            if not route.sysadmin:
                capability = self.manager.api.capabilities.list(
                    application_id=self.application_id, route_id=route.id)
                self.manager.api.policies.create(
                    capability_id=capability[0].id, role_id=self.entity.id)

        return self.entity


class CreateWithGrantedResources(operation.Operation):

    def pre(self, **kwargs):

        applications = self.manager.api.applications.list(name='default')
        if not applications:
            raise exception.OperationBadRequest()

        self.application_id = applications[0].id
        self.name = kwargs.get('name')
        self.tag = None
        if 'tag' in kwargs:
            self.tag = kwargs.get('tag')
        self.granted_resources = kwargs.get('granted_resources')

        if ((self.application_id is None) or (self.name is None) or
           (self.granted_resources is None)):
            raise exception.OperationBadRequest()

        return True

    def do(self, session, **kwargs):

        self.entity = self.manager.api.roles.create(
            name=self.name, tag=self.tag)

        routes = self.manager.api.routes.list()

        for route in routes:
            if (not route.sysadmin) and (route.url in self.granted_resources):
                capability = self.manager.api.capabilities.list(
                    application_id=self.application_id, route_id=route.id)
                self.manager.api.policies.create(
                    capability_id=capability[0].id, role_id=self.entity.id)

        return self.entity


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.createAdmin = CreateAdmin(self)
        self.createWithGrantedResources = CreateWithGrantedResources(self)
