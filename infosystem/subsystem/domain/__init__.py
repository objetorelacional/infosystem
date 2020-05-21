from infosystem.common import subsystem
from infosystem.subsystem.domain import manager, resource, controller, router

subsystem = subsystem.Subsystem(resource=resource.Domain,
                                manager=manager.Manager,
                                controller=controller.Controller,
                                router=router.Router)
