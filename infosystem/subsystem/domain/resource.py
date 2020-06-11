from infosystem.database import db
from infosystem.common.subsystem import entity


class Domain(entity.Entity, db.Model):

    attributes = ['name', 'parent_id', 'application_id']
    attributes += entity.Entity.attributes

    application_id = db.Column(
        db.CHAR(32), db.ForeignKey("application.id"), nullable=False)
    name = db.Column(db.String(60), nullable=False, unique=True)
    parent_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=True)

    def __init__(self, id, application_id, name, parent_id=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.application_id = application_id
        self.name = name
        self.parent_id = parent_id
