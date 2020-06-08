from infosystem.database import db
from infosystem.common.subsystem import entity
from sqlalchemy import orm


class Grant(entity.Entity, db.Model):

    attributes = ['user_id', 'role_id']
    attributes += entity.Entity.attributes

    user_id = db.Column(
        db.CHAR(32), db.ForeignKey("infosystem.user.id"), nullable=False)
    user = orm.relationship("User", backref=orm.backref('grants'))
    role_id = db.Column(db.CHAR(32),
                        db.ForeignKey("infosystem.role.id"),
                        nullable=False)
    role = orm.relationship("Role", backref=orm.backref('grants'))

    __table_args__ = {'schema': 'infosystem'}

    def __init__(self, id, user_id, role_id,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.user_id = user_id
        self.role_id = role_id
