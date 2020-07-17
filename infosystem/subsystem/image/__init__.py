from infosystem.common import subsystem
from infosystem.subsystem.image import resource, manager, controller, router

subsystem = subsystem.Subsystem(resource=resource.Image,
                                manager=manager.Manager,
                                controller=controller.Controller,
                                router=router.Router)
