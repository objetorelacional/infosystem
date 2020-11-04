from enum import Enum
from decimal import Decimal
from datetime import datetime

from infosystem.database import db

DATE_FMT = '%Y-%m-%d'
DATETIME_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'


class Entity(object):

    attributes = ['id', 'active', 'created_at', 'created_by',
                  'updated_at', 'updated_by', 'tag']

    id = db.Column(db.CHAR(32), primary_key=True, autoincrement=False)
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.CHAR(32))
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.CHAR(32))
    tag = db.Column(db.String(1000))

    def __init__(self, id, active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        self.id = id
        self.active = active
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.tag = tag

    @classmethod
    def embedded(cls):
        return []

    @classmethod
    def individual(cls):
        return cls.__name__.lower()

    @classmethod
    def collection(cls):
        return cls.individual() + 's'

    def is_stable(self):
        return True

    def allDateFmtFromAllTypes(self, dateOrDateTime):
        dateTime = None
        if dateOrDateTime is not None:
            if type(dateOrDateTime) is str:
                try:
                    if len(dateOrDateTime.strip()) == 10:
                        dateTime = datetime.strptime(
                            dateOrDateTime, DATE_FMT)
                    elif len(dateOrDateTime.strip()) == 24:
                        dateTime = datetime.strptime(
                            dateOrDateTime, DATETIME_FMT)
                except Exception:
                    pass
            else:
                if type(dateOrDateTime) is datetime:
                    dateTime = dateOrDateTime

        return dateTime

    def convert_numeric(self, value):
        if str(value).find('.') > -1:
            return float(value.real)
        else:
            return int(value)

    def to_dict(self, include_dict=None, stringify=True):
        d = {}
        include_dict = include_dict or {}

        for attr in self.__class__.attributes:
            if attr not in include_dict:
                value = getattr(self, attr)
                if value is not None:
                    if isinstance(value, Enum):
                        d[attr] = value.name
                    elif isinstance(value, Decimal):
                        d[attr] = self.convert_numeric(value)
                    elif isinstance(value, Entity):
                        include_dict.update({attr: {}})
                    else:
                        d[attr] = value
                # TODO(fdoliveira) Why change format of date and datetime?
                # if stringify and isinstance(value, datetime):
                #    d[attr] = value.strftime(DATETIME_FMT)
                # elif stringify and isinstance(value, date):
                #    d[attr] = value.strftime(DATETIME_FMT)
                # else:

        # Only embedded that are not in include will be updated
        # include_dict.update({attr: {} for attr in self.embedded()})
        for attr in self.embedded():
            if attr not in include_dict:
                include_dict.update({attr: {}})

        if include_dict:
            for key, value in include_dict.items():
                if not isinstance(value, dict):
                    # it's a filter
                    if getattr(self, key) != value:
                        raise AssertionError()
                    continue

                thing = getattr(self, key)
                if isinstance(thing, list):
                    values = []
                    empty = True
                    for part in thing:
                        try:
                            values.append(part.to_dict(value))
                            empty = False
                        except AssertionError:
                            # filter mismatch, ignore the expansion
                            pass
                    if values and empty:
                        # filter mismatch, no entity matched the filter,
                        # re-raise and ignore current entity
                        raise AssertionError()
                    d[key] = [part.to_dict(value) for part in thing]
                else:
                    try:
                        if thing is not None:
                            d[key] = thing.to_dict(value)
                    except AssertionError:
                        # filter mismatch, re-raise to ignore current entity
                        raise

        return d
