from celery.app.utils import Settings
from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        settings_endpoint = '/settings'
        return super().routes + [
            {
                'action': 'Get Domain By Name',
                'method': 'GET',
                'url': '/domainbyname',
                'callback': self.controller.domain_by_name,
                'bypass': True
            },
            {
                'action': 'Get Domain Logo By Name',
                'method': 'GET',
                'url': '/domainlogobyname',
                'callback': self.controller.domain_logo_by_name,
                'bypass': True
            },
            {
                'action': 'Upload logo to Domain',
                'method': 'PUT',
                'url': self.resource_url + '/logo',
                'callback': self.controller.upload_logo
            },
            {
                'action': 'Remove logo from Domain',
                'method': 'DELETE',
                'url': self.resource_url + '/logo',
                'callback': self.controller.remove_logo
            },
            {
                'action': 'Register new Domain',
                'method': 'POST',
                'url': self.collection_url + '/register',
                'callback': self.controller.register,
                'bypass': True
            },
            {
                'action': 'Activate a register Domain',
                'method': 'PUT',
                'url': self.resource_enum_url + '/activate/<id2>',
                'callback': self.controller.activate,
                'bypass': True
            },
            {
                'action': 'Create settings on Domain',
                'method': 'POST',
                'url': self.resource_url + settings_endpoint,
                'callback': self.controller.create_settings,
                'bypass': False
            },
            {
                'action': 'Update settings on Domain',
                'method': 'PUT',
                'url': self.resource_url + settings_endpoint,
                'callback': self.controller.update_settings,
                'bypass': False
            },
            {
                'action': 'Remove settings from Domain',
                'method': 'DELETE',
                'url': self.resource_url + settings_endpoint,
                'callback': self.controller.remove_settings,
                'bypass': False
            },
            {
                'action': 'Get settings by keys from Domain',
                'method': 'GET',
                'url': self.resource_url + settings_endpoint,
                'callback': self.controller.get_domain_settings_by_keys,
                'bypass': False
            }
        ]
