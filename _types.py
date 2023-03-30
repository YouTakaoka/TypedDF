import datetime
import pandas as pd
from pandas import Timestamp, Timedelta, Period
from typing import TypedDict, TypeVar, TypeAlias, Union, Hashable
import re

SCALAR_NAME: TypeAlias = Union[str, int, bool, float, bytes, complex]
_DEFAULT_TYPE: SCALAR_NAME = 'str'
_TYPE_NAME_TABLE: list[tuple[str, SCALAR_NAME]] = [
    (r'int(|[0-9]*)', 'int'),
    (r'float(|[0-9]*)', 'float'),
    ('bool', 'bool'),
    ('object', 'str')
]
def conv_typename(name: str) -> SCALAR_NAME:
    for p, n in _TYPE_NAME_TABLE:
        if re.fullmatch(p, name):
            return n
    return _DEFAULT_TYPE

S1 = TypeVar(
    'S1',
    str,
    bytes,
    bool,
    int,
    float,
    complex,
    datetime.date,
    datetime.datetime,
    datetime.time,
    Timedelta,
    Timestamp,
    Period,
)
TD = TypeVar('TD', bound = TypedDict)
H = TypeVar('H', bound=Hashable)

def get_datatypes(df: pd.DataFrame) -> dict[str, SCALAR_NAME]:
    return {k: conv_typename(str(t)) for k, t in df.dtypes.to_dict().items()}