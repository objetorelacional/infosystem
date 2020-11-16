from typing import Any
from sqlalchemy import orm
from sqlalchemy_json import NestedMutableJson

from infosystem.database import db
from infosystem.common.subsystem import entity
from infosystem.common import exception


class Domain(entity.Entity, db.Model):

    DEFAULT = 'default'

    attributes = ['name', 'display_name', 'parent_id',
                  'application_id', 'logo_id', 'doc', 'description', 'settings']
    attributes += entity.Entity.attributes

    application_id = db.Column(
        db.CHAR(32), db.ForeignKey("application.id"), nullable=False)
    application = orm.relationship('Application', backref=orm.backref(
        'domains'))
    name = db.Column(db.String(60), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)
    doc = db.Column(db.String(60), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    logo_id = db.Column(db.CHAR(32), db.ForeignKey('image.id'), nullable=True)
    parent_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=True)
    addresses = orm.relationship(
        'DomainAddress', backref=orm.backref('domain_addresses'),
        cascade='delete,delete-orphan,save-update')
    contacts = orm.relationship(
        'DomainContact', backref=orm.backref('domain_contacts'),
        cascade='delete,delete-orphan,save-update')
    _settings = db.Column(NestedMutableJson, nullable=False, default={})

    __tablename__ = 'domain'

    def __init__(self, id, application_id, name, display_name=None,
                 doc=None, description=None, logo_id=None, parent_id=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.application_id = application_id
        self.name = name
        if display_name is None:
            self.display_name = name
        else:
            self.display_name = display_name
        self.doc = doc
        self.description = description
        self.logo_id = logo_id
        self.parent_id = parent_id

    def _get_setting(self, setting_id: str):
        setting = next((s for s in self.settings if s.id == setting_id), None)

        if not setting:
            raise exception.NotFound(
                'Erro! Setting não encontrado nesse domínio')
        return setting

    def _has_setting(self, key: str) -> bool:
        return self._settings.get(key) is not None

    def remove_setting(self, key: str):
        if not self._has_setting(key):
            raise exception.BadRequest(f"Erro! Setting {key} not exists")

        value = self._settings.pop(key)
        return value

    def create_setting(self, key: str, value: Any):
        if self._has_setting(key):
            raise exception.BadRequest(f"Erro! Setting {key} already exists")

        self._settings[key] = value
        return value

    def update_setting(self, key: str, value: Any):
        if not self._has_setting(key):
            raise exception.BadRequest(f"Erro! Setting {key} not exists")

        self._settings[key] = value
        return value

    @property
    def settings(self):
        return self._settings

    @classmethod
    def embedded(cls):
        return ['addresses', 'contacts']


class DomainAddress(entity.Entity, db.Model):

    attributes = ['postal_code', 'address_line_1', 'address_line_2',
                  'city', 'state_province', 'country', 'tag']

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain.id'), nullable=False)
    postal_code = db.Column(db.String(30), nullable=False)
    address_line_1 = db.Column(db.String(255), nullable=False)
    address_line_2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state_province = db.Column(db.String(60), nullable=False)
    country = db.Column(db.String(60), nullable=False)

    def __init__(self, id, domain_id, postal_code, address_line_1,
                 city, state_province, country, address_line_2=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_id = domain_id
        self.postal_code = postal_code
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state_province = state_province
        self.country = country


class DomainContact(entity.Entity, db.Model):

    attributes = ['contact', 'tag']

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    contact = db.Column(db.String(100), nullable=False)

    def __init__(self, id, domain_id, contact,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_id = domain_id
        self.contact = contact
