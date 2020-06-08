from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class Route(entity.Entity, db.Model):

    attributes = ['name', 'url', 'method', 'sysadmin', 'bypass']
    attributes += entity.Entity.attributes

    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    bypass = db.Column(db.Boolean(), nullable=False)
    sysadmin = db.Column(db.Boolean(), nullable=False)

    __table_args__ = (UniqueConstraint('url', 'method', name='route_uk'),
                      {'schema': 'infosystem'})

    def __init__(self, id, name, url, method, bypass=False, sysadmin=False,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.name = name
        self.url = url
        self.method = method
        self.bypass = bypass
        self.sysadmin = sysadmin
