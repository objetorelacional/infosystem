from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        return super().routes + [
            {
                'action': 'get_by_name',
                'method': 'GET',
                'url': '/domainbyname',
                'callback': self.controller.get_by_name,
                'bypass': True
            }
        ]
