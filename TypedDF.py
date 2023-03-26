"""`pandas.DataFrame` with type

Module contains `TypedDF` class and some utility functions for the class.
`TypedDF` is a subclass of `pandas.DataFrame` which can be used with static typecheckers.
"""

from typing import TypedDict, TypeVar, Generic, TypeGuard, Type, TypeAlias, Union, Dict
import pandas as pd
from pandas import Timestamp, Timedelta, Period
import yaml
import re
import datetime

_SCALAR_NAME: TypeAlias = Union[str, int, bool, float, bytes, complex]
_DEFAULT_TYPE: _SCALAR_NAME = 'str'
_TYPE_NAME_TABLE: list[tuple[str, _SCALAR_NAME]] = [
    (r'int(|[0-9]*)', 'int'),
    (r'float(|[0-9]*)', 'float'),
    ('bool', 'bool'),
    ('object', 'str')
]

U_S1: TypeAlias = Union[
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
]
B1 = TypeVar('B1', bound=U_S1)
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
SCALAR: list[type] = [str, int, bool, float, bytes, complex]
S = TypeVar(
    'S',
    str,
    int,
    bool,
    float,
    bytes,
    complex,
)
T = TypeVar('T', bound = TypedDict)
TD = TypeVar('TD', bound = Dict[str, U_S1])

def _conv_typename(name: str) -> _SCALAR_NAME:
    for p, n in _TYPE_NAME_TABLE:
        if re.fullmatch(p, name):
            return n
    return _DEFAULT_TYPE

def _get_datatypes(df: pd.DataFrame) -> dict[str, _SCALAR_NAME]:
    return {k: _conv_typename(str(t)) for k, t in df.dtypes.to_dict().items()}


class TypedDF(pd.DataFrame, Generic[T]):
    """`pandas.DataFrame` with type
    
    Subclass of `pandas.DataFrame` which can be used with static typecheckers.
    """
    
    @classmethod
    def from_df(cls, td: Type[T], df: pd.DataFrame) -> 'TypedDF[T]':
        """Converts `pandas.DataFrame` to `TypedDF`.

        Performs runtime typecheck for the passed `pandas.DataFrame` and converts it to an instance of `TypedDF`.
        If the function fails to typecheck, it raises `TypeError`.

        Args:
            td (Type[T]): A subclass of `type.TypedDict`.
            df (pandas.DataFrame): `pandas.DataFrame` as the source.

        Returns:
            TypedDF: Resulting `TypedDF`
        """

        def _typecheck(df: pd.DataFrame) -> TypeGuard[TypedDF[T]]:
            datatypes: dict[str, _SCALAR_NAME] = _get_datatypes(df)
            dt: dict[str, str] = {k: v.__name__ for k, v in td.__annotations__.items()}
            return datatypes == dt
        
        if not _typecheck(df):
            raise TypeError('Typecheck failed.')
        
        return df

    @classmethod
    def gen_classdef(cls, df: pd.DataFrame, class_name: str) -> str:
        """Generates Python code of class definition from `pandas.DataFrame`.

        Derives type data from passed `pandas.DataFrame` and generates Python code of class definition, which is subclass of `type.TypedDict`.
        The resulting class can be specified at the first argument of `from_df()`.

        Args:
            df (pandas.DataFrame): `pandas.DataFrame` from which the type data would be derived.
            class_name (str): Name of the new class.
        
        Returns:
            str: Python code of class definition.
        """

        key: str = 'class {}(TypedDict)'.format(class_name)
        return yaml.dump({key: _get_datatypes(df)}, indent=4)

    @classmethod
    def save_classdef(cls, df: pd.DataFrame, class_name: str, file_name: str | None = None) -> None:
        """Saves Python code of class definition from `pandas.DataFrame`.

        Derives type data from passed `pandas.DataFrame` and saves Python code of class definition, which is subclass of `type.TypedDict`.
        The resulting class can be specified at the first argument of `from_df()`.
        If `file_name` parameter is not specified, `class_name` will be used for the name of Python file.

        Args:
            df (pandas.DataFrame): `pandas.DataFrame` from which the type data would be derived.
            class_name (str): Name of the new class.
            file_name (str): Name of Python file to be saved.
        """

        import_line: str = 'from typing import TypedDict\n\n'
        s: str = import_line + cls.gen_classdef(df, class_name)
        fname: str = '{}.py'.format(class_name)
        if file_name:
            fname = file_name 

        with open(fname, mode='w') as fp:
            fp.write(s)
