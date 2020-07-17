from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        return [
            {
                'action': 'create',
                'method': 'POST',
                'url': self.collection_url,
                'callback': self.controller.create
            },
            {
                'action': 'get',
                'method': 'GET',
                'bypass': True,
                'url': self.resource_url,
                'callback': self.controller.get
            },
            {
                'action': 'list',
                'method': 'GET',
                'url': self.collection_url,
                'callback': self.controller.list
            },
            {
                'action': 'update',
                'method': 'PUT',
                'url': self.resource_url,
                'callback': self.controller.update
            },
            {
                'action': 'delete',
                'method': 'DELETE',
                'url': self.resource_url,
                'callback': self.controller.delete
            }
        ]
