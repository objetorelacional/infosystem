from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class Capability(entity.Entity, db.Model):

    attributes = ['route_id', 'domain_id']
    attributes += entity.Entity.attributes

    route_id = db.Column(
        db.CHAR(32), db.ForeignKey("infosystem.route.id"), nullable=False)
    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey("infosystem.domain.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('route_id', 'domain_id', name='capability_uk'),
        {'schema': 'infosystem'})

    def __init__(self, id, route_id, domain_id,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.route_id = route_id
        self.domain_id = domain_id

    @classmethod
    def collection(cls):
        return 'capabilities'
