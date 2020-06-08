from datetime import datetime
from infosystem.database import db
from infosystem.common.subsystem import entity


class Notification(entity.Entity, db.Model):

    attributes = ['user_id', 'date', 'subject', 'body', 'read_date']
    attributes += entity.Entity.attributes

    user_id = db.Column(
        db.CHAR(32), db.ForeignKey("infosystem.user.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    read_date = db.Column(db.Date, nullable=True)

    __table_args__ = {'schema': 'infosystem'}

    def __init__(self, id, user_id, date, subject, body, active=True,
                 read_date=None, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.user_id = user_id
        self.date = datetime.strptime(date, entity.DATETIME_FMT)
        self.subject = subject
        self.body = body
        if (read_date is not None):
            self.read_date = datetime.strptime(read_date, entity.DATETIME_FMT)
