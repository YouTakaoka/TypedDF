"""`pandas.DataFrame` with type

Module contains `TypedDF` class and some utility functions for the class.
`TypedDF` is a subclass of `pandas.DataFrame` which can be used with static typecheckers.
"""

from typing import TypedDict, TypeVar, Generic, TypeGuard, Type, TypeAlias, Union, Hashable
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

def _conv_typename(name: str) -> _SCALAR_NAME:
    for p, n in _TYPE_NAME_TABLE:
        if re.fullmatch(p, name):
            return n
    return _DEFAULT_TYPE

class TypedDF(pd.DataFrame, Generic[TD]):
    """`pandas.DataFrame` with type
    
    Subclass of `pandas.DataFrame` which can be used with static typecheckers.
    """

    @classmethod
    def _get_datatypes(cls, df: pd.DataFrame) -> dict[str, _SCALAR_NAME]:
        return {k: _conv_typename(str(t)) for k, t in df.dtypes.to_dict().items()}
    
    @classmethod
    def from_df(cls, df: pd.DataFrame, td: Type[TD]) -> 'TypedDF[TD]':
        """Converts `pandas.DataFrame` to `TypedDF`.

        Performs runtime typecheck for the passed `pandas.DataFrame` and converts it to an instance of `TypedDF`.
        If the function fails to typecheck, it raises `TypeError`.

        Args:
            td (Type[T]): A subclass of `type.TypedDict`.
            df (pandas.DataFrame): `pandas.DataFrame` as the source.

        Returns:
            TypedDF: Resulting `TypedDF`
        """

        def _typecheck(df: pd.DataFrame) -> TypeGuard[TypedDF[TD]]:
            datatypes: dict[str, _SCALAR_NAME] = cls._get_datatypes(df)
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
        return yaml.dump({key: cls._get_datatypes(df)}, indent=4)

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

class GenericSeries(pd.Series, Generic[S1]):
    @classmethod
    def from_series(cls, s: pd.Series, t: Type[S1]) -> "GenericSeries[S1]":
        def _typecheck(s: pd.Series) -> TypeGuard[GenericSeries[S1]]:
            return _conv_typename(str(s.dtype)) == t.__name__
        
        if not _typecheck(s):
            raise TypeError('Typecheck failed.')
        
        return s

class TypedSeries(pd.Series, Generic[TD]):
    @classmethod
    def from_series(cls, s: pd.Series, td: Type[TD]) -> "TypedSeries[TD]":
        def _typecheck(s: pd.Series) -> TypeGuard[TypedSeries[TD]]:
            for k, item in s.items():
                if not isinstance(item, td.__annotations__[str(k)]):
                    return False
            return True
        
        if not _typecheck(s):
            raise TypeError('Typecheck failed.')
        
        return s

class GenericIndex(pd.Index, Generic[H]):
    @classmethod
    def from_index(cls, idx: pd.Index, t: Type[H]) -> "GenericIndex[H]":
        def _typecheck(idx: pd.Index) -> TypeGuard[GenericIndex[H]]:
            return _conv_typename(str(idx.dtype)) == t.__name__

        if not _typecheck(idx):
            raise TypeError('Typecheck failed.')
        
        return idx
    
class TypedMultiIndex(pd.MultiIndex, Generic[TD]):
    @classmethod
    def from_index(cls, idx: pd.Index, td: Type[TD]) -> "TypedMultiIndex[TD]":
        def _get_datatypes(idx: pd.Index) -> dict[str, Type]:
            return {str(k): _conv_typename(str(t)) for k, t in idx.dtypes.to_dict().items()}
        
        def _typecheck(idx: pd.Index) -> TypeGuard[TypedMultiIndex[TD]]:
            datatypes: dict[str, Type] = _get_datatypes(idx)
            dt: dict[str, str] = {k: v.__name__ for k, v in td.__annotations__.items()}
            return datatypes == dt
        
        if not _typecheck(idx):
            raise TypeError('Typecheck failed.')
        
        return idx
