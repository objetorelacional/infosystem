from infosystem.common import subsystem
from infosystem.subsystem.application import resource, manager, controller, \
    router

subsystem = subsystem.Subsystem(resource=resource.Application,
                                manager=manager.Manager,
                                controller=controller.Controller,
                                router=router.Router)
