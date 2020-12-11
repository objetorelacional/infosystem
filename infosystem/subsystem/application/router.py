from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        return super().routes + [
            {
                'action': 'getApplicationRoles',
                'method': 'GET',
                'url': self.resource_url + '/roles',
                'callback': self.controller.get_roles
            }
        ]
