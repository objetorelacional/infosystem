from datetime import datetime
from infosystem.database import db
from infosystem.common.subsystem import entity


class Token(entity.Entity, db.Model):

    attributes = ['user_id']
    attributes += entity.Entity.attributes

    user_id = db.Column(
        db.CHAR(32), db.ForeignKey("infosystem.user.id"), nullable=False)

    __table_args__ = {'schema': 'infosystem'}

    def __init__(self, id, user_id, active=True, created_at=datetime.now(),
                 created_by=user_id, updated_at=None,
                 updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.user_id = user_id
