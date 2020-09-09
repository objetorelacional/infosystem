import json

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Union, Any
import uuid

DATE_FMT = '%Y-%m-%d'
DATETIME_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'


def convert_date_from_str(value: Optional[str]) -> Optional[datetime]:
    date_time = None
    if value is not None:
        try:
            if len(value.strip()) == 10:
                date_time = datetime.strptime(value, DATE_FMT)
            elif len(value.strip()) == 24:
                date_time = datetime.strptime(value, DATETIME_FMT)
        except Exception:
            pass
    return date_time


def convert_date_to_str(date_value: Union[date, datetime]) -> str:
    if type(date_value) is date:
        return date_value.strftime(DATE_FMT)
    elif type(date_value) is datetime:
        return date_value.strftime(DATETIME_FMT)
    else:
        raise Exception('{} is not date or datetime'.format(date_value))


def convert_decimal(value: Decimal) -> Union[float, int]:
    if isinstance(value, Decimal):
        if not value.is_finite():
            return str(value)
        if str(value).find('.') > -1:
            return float(value.real)
        else:
            return int(value)
    else:
        raise Exception('{} is not Decimal'.format(value))


class InfosystemEncoder(json.JSONEncoder):

    def default(self, value: Any) -> Any:
        try:
            if isinstance(value, Decimal):
                return convert_decimal(value)
            if isinstance(value, date):
                return convert_date_to_str(value)
            if isinstance(value, Enum):
                return value.name

            # default  str
            return str(value)
        except Exception:
            return super().default(value)


def to_json(value: Any) -> str:
    return json.dumps(value, cls=InfosystemEncoder)


def random_uuid() -> str:
    return uuid.uuid4().hex
