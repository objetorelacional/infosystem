from infosystem.common import subsystem
from infosystem.subsystem.route import resource, manager


subsystem = subsystem.Subsystem(resource=resource.Route,
                                manager=manager.Manager)
