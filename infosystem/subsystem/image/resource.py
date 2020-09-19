import enum

from infosystem.database import db
from infosystem.subsystem.file.resource import File


class QualityImage(enum.Enum):
    min = 'MIN'
    med = 'MED'
    max = 'MAX'


class Image(File, db.Model):
    attributes = []
    attributes += File.attributes

    id = db.Column(db.ForeignKey('file_infosys.id'), primary_key=True)
    type_image = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'image'}

    def __init__(self, id, domain_id, name, type_image='', active=True,
                 created_at=None, created_by=None, updated_at=None,
                 updated_by=None, tag=None):
        super().__init__(id, domain_id, name, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.type_image = type_image

    @classmethod
    def collection(cls):
        return 'images'

    def filename_with_quality(self, quality: QualityImage):
        if quality is None:
            return '{}.{}'.format(self.id, 'jpg')
        else:
            return '{}.{}.{}'.format(self.id, quality.value, 'jpg')
