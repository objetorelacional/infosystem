from infosystem.database import db
from infosystem.common.subsystem import entity


class File(entity.Entity, db.Model):

    # TODO(fdoliveira) Check in another databases
    # This is required because Oracle dont accept FILE for table name
    __tablename__ = 'file_infosys'

    attributes = ['domain_id', 'name']
    attributes += entity.Entity.attributes

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=True)
    name = db.Column(db.String(255), nullable=True)

    def __init__(self, id, domain_id, name,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_id = domain_id
        self.name = name

    @property
    def extension(self):
        name = self.name.split('.')
        return name[-1]

    @property
    def filename(self):
        return '{}.{}'.format(self.id, self.extension)
