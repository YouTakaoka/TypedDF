import datetime
import pandas as pd
from pandas import Timestamp, Timedelta, Period
from typing import TypedDict, TypeVar, TypeAlias, Union, Hashable, Type, Generic, Iterable, Iterator, List, Tuple
from typing_extensions import TypeVarTuple, Unpack
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
H = TypeVar('H', bound = Hashable)
_T_co = TypeVar('_T_co', covariant=True)

class CoList(Iterable[_T_co], Generic[_T_co]):
    def __init__(self, items: Iterable[_T_co]) -> None:
        self._items: Iterable[_T_co] = items

    def __iter__(self) -> Iterator[_T_co]:
        return self._items.__iter__()
    
    def to_list(self) -> List[_T_co]:
        return list(self._items)

H1 = TypeVar('H1', bound = CoList[Type[Hashable]])
H2 = TypeVar('H2', bound = tuple[Type[Hashable], ...])

Ts = TypeVarTuple('Ts')

class TypeTuple(Tuple[Type], Generic[Unpack[Ts]]):
    def __new__(cls, *args: Type[Hashable]) -> "TypeTuple[Unpack[Ts]]":
        Ts = args
        return super().__new__(cls, args)

tt = TypeTuple(str, int)

def get_datatypes(df: pd.DataFrame) -> dict[str, SCALAR_NAME]:
    return {k: conv_typename(str(t)) for k, t in df.dtypes.to_dict().items()}
