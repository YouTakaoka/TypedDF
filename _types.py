import datetime
import pandas as pd
from pandas import Timestamp, Timedelta, Period
from typing import NamedTuple, TypeVar, TypeAlias, Union, Hashable, Type, Generic, Iterable, Iterator, List, Tuple, NewType, Literal
from typing_extensions import TypeVarTuple, Unpack, Self
from enum import Enum
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

IDX = TypeVar("IDX", bound = Hashable | NamedTuple)

def get_datatypes(df: pd.DataFrame) -> dict[str, SCALAR_NAME]:
    return {k: conv_typename(str(t)) for k, t in df.dtypes.to_dict().items()}
