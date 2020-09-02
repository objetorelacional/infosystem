from infosystem.common import subsystem
from infosystem.subsystem.domain import manager, resource, controller, router

subsystem = subsystem.Subsystem(resource=resource.Domain,
                                controller=controller.Controller,
                                manager=manager.Manager,
                                router=router.Router)
