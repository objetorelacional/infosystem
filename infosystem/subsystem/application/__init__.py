from infosystem.common import subsystem
from infosystem.common.subsystem import controller, router
from infosystem.subsystem.application import resource, manager

subsystem = subsystem.Subsystem(resource=resource.Application,
                                manager=manager.Manager,
                                controller=controller.Controller,
                                router=router.Router)
