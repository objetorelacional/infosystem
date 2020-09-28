from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
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
                'action': 'Create a setting Domain',
                'method': 'POST',
                'url': self.resource_url + '/settings',
                'callback': self.controller.create_setting,
                'bypass': False
            },
            {
                'action': 'Update a setting Domain',
                'method': 'PUT',
                'url': self.resource_enum_url + '/settings/<id2>',
                'callback': self.controller.update_setting,
                'bypass': False
            },
            {
                'action': 'Remove a setting Domain',
                'method': 'DELETE',
                'url': self.resource_enum_url + '/settings/<id2>',
                'callback': self.controller.remove_setting,
                'bypass': False
            }
        ]
