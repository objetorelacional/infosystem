from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class Application(entity.Entity, db.Model):

    DEFAULT = "default"

    attributes = ['name', 'description']
    attributes += entity.Entity.attributes

    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    __table_args__ = (UniqueConstraint('name', name='application_name_uk'),)

    def __init__(self, id, name, description,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.name = name
        self.description = description
