
class Router(object):

    def __init__(self, controller, collection, routes=[]):
        self.controller = controller

        self.collection_url = '/' + collection
        self.resource_url = self.collection_url + '/<id>'
        self.resource_enum_url = self.resource_url.replace('<id>', '<id1>')

        if routes:
            self._routes = [
                r for r in self.get_crud() if r['action'] in routes]
        else:
            self._routes = self.get_crud()

    def get_crud(self):
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

    @property
    def routes(self):
        return self._routes
