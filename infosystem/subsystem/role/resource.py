from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class Role(entity.Entity, db.Model):

    USER = 'User'
    SYSADMIN = 'Sysadmin'
    ADMIN = 'Admin'

    attributes = ['name']
    attributes += entity.Entity.attributes

    name = db.Column(db.String(80), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='role_name_uk'),)

    def __init__(self, id, name,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.name = name
