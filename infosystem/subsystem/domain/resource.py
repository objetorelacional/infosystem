from infosystem.database import db
from infosystem.common.subsystem import entity


class Domain(entity.Entity, db.Model):

    attributes = ['name', 'parent_id']
    attributes += entity.Entity.attributes

    name = db.Column(db.String(60), nullable=False, unique=True)
    parent_id = db.Column(
        db.CHAR(32), db.ForeignKey("infosystem.domain.id"), nullable=True)

    __table_args__ = {'schema': 'infosystem'}

    def __init__(self, id, name, parent_id=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.name = name
        self.parent_id = parent_id
