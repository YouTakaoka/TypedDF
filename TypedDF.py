"""`pandas.DataFrame` with type

Module contains `TypedDF` class and some utility functions for the class.
`TypedDF` is a subclass of `pandas.DataFrame` which can be used with static typecheckers.
"""

from typing import TypedDict, TypeVar, Generic, TypeGuard, Type
import pandas as pd
import yaml
import re

DEFAULT_TYPE: str = 'str'
TYPE_NAME_TABLE: list[tuple[str, str]] = [
    (r'int(|[0-9]*)', 'int'),
    (r'float(|[0-9]*)', 'float'),
    ('bool', 'bool'),
    ('object', 'str')
]

def _conv_typename(name: str) -> str:
    for p, n in TYPE_NAME_TABLE:
        if re.fullmatch(p, name):
            return n
    return DEFAULT_TYPE

def _get_datatypes(df: pd.DataFrame) -> dict[str, str]:
    return {k: _conv_typename(str(v)) for k, v in df.dtypes.to_dict().items()}

T = TypeVar('T', bound = TypedDict)

class TypedDF(pd.DataFrame, Generic[T]):
    """`pandas.DataFrame` with type
    
    Subclass of `pandas.DataFrame` which can be used with static typecheckers.
    """
    pass
 
def from_df(td: Type[T], df: pd.DataFrame) -> TypedDF[T]:
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
        datatypes: dict[str, str] = _get_datatypes(df)
        dt: dict[str, str] = {k: v.__name__ for k, v in td.__annotations__.items()}
        return datatypes == dt
    
    if not _typecheck(df):
        raise TypeError('Typecheck failed.')
    
    return df

def gen_classdef(df: pd.DataFrame, class_name: str) -> str:
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

def save_classdef(df: pd.DataFrame, class_name: str, file_name: str | None = None) -> None:
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
    s: str = import_line + gen_classdef(df, class_name)
    fname: str = '{}.py'.format(class_name)
    if file_name:
        fname = file_name 

    with open(fname, mode='w') as fp:
        fp.write(s)
