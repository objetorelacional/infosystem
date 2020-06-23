from infosystem.common import subsystem
from infosystem.subsystem.image import resource, manager, controller

subsystem = subsystem.Subsystem(resource=resource.Image,
                                manager=manager.Manager,
                                controller=controller.Controller)
