from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        return [
            {
                'action': 'register',
                'method': 'POST',
                'url': '/register',
                'callback': self.controller.register,
                'bypass': True
            },
            {
                'action': 'activate',
                'method': 'POST',
                'url': '/activate',
                'callback': self.controller.activate,
                'bypass': True
            }
        ]
