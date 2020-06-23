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
            {'action': 'reset', 'method': 'POST',
                'url': self.collection_url + '/reset',
                'callback': self.controller.reset},
            {'action': 'routes', 'method': 'GET',
                'url': self.collection_url + '/routes',
                'callback': self.controller.routes},

            {'action': 'routes', 'method': 'PUT',
                'url': self.resource_url + '/photo',
                'callback': self.controller.upload_photo},
            {'action': 'routes', 'method': 'DELETE',
                'url': self.resource_url + '/photo',
                'callback': self.controller.delete_photo}
        ]
