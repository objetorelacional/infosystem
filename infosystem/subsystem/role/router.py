from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        return super().routes + [
            {
                'action': 'createPolicies',
                'method': 'POST',
                'url': self.resource_url + '/policies',
                'callback': self.controller.create_policies
            }
        ]
