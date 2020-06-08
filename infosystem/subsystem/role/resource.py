from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class Role(entity.Entity, db.Model):

    attributes = ['domain_id', 'name']
    attributes += entity.Entity.attributes

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey("infosystem.domain.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    __table_args__ = (
        UniqueConstraint('domain_id', 'name', name='role_name_uk'),
        {'schema': 'infosystem'})

    def __init__(self, id, domain_id, name,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_id = domain_id
        self.name = name
