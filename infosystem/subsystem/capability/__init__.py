from infosystem.common import subsystem
from infosystem.subsystem.capability import resource, manager


subsystem = subsystem.Subsystem(resource=resource.Capability,
                                manager=manager.Manager)
