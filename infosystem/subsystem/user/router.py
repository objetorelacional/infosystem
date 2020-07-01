from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        return super().routes + [
            {'action': 'restore', 'method': 'POST',
                'url': self.collection_url + '/restore',
                'callback': self.controller.restore, 'bypass': True},

            {'action': 'reset_password', 'method': 'POST',
                'url': self.resource_url + '/reset',
                'callback': self.controller.reset_password},
            {'action': 'reset_my_password', 'method': 'POST',
                'url': self.collection_url + '/reset',
                'callback': self.controller.reset_my_password},
            {'action': 'update_my_password', 'method': 'PUT',
                'url': self.resource_url + '/update_my_password',
                'callback': self.controller.update_password},

            {'action': 'routes', 'method': 'GET',
                'url': self.collection_url + '/routes',
                'callback': self.controller.routes},

            {'action': 'routes', 'method': 'PUT',
                'url': self.resource_url + '/photo',
                'callback': self.controller.upload_photo},
            {'action': 'routes', 'method': 'DELETE',
                'url': self.resource_url + '/photo',
                'callback': self.controller.delete_photo},
            {'action': 'notify', 'method': 'POST',
                'url': self.resource_url + '/notify',
                'callback': self.controller.notify}
        ]
