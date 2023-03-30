"""`pandas.DataFrame` with type

Module contains `TypedDF` class and some utility functions for the class.
`TypedDF` is a subclass of `pandas.DataFrame` which can be used with static typecheckers.
"""

import yaml

from TypedIndex import *

class TypedDF(pd.DataFrame, Generic[IDX, TD]):
    """`pandas.DataFrame` with type
    
    Subclass of `pandas.DataFrame` which can be used with static typecheckers.
    """
    
    def __new__(cls, df: pd.DataFrame, td: Type[TD], index_type: IDX = GIT_INT) -> 'TypedDF[IDX, TD]':
        """Converts `pandas.DataFrame` to `TypedDF`.

        Performs runtime typecheck for the passed `pandas.DataFrame` and converts it to an instance of `TypedDF`.
        If the function fails to typecheck, it raises `TypeError`.

        Args:
            td (Type[T]): A subclass of `type.TypedDict`.
            df (pandas.DataFrame): `pandas.DataFrame` as the source.

        Returns:
            TypedDF: Resulting `TypedDF`
        """

        def _typecheck(df: pd.DataFrame) -> TypeGuard[TypedDF[IDX, TD]]:
            dt: dict[str, str] = {k: v.__name__ for k, v in td.__annotations__.items()}
            return get_datatypes(df) == dt
        
        if not _typecheck(df):
            raise TypeError('Typecheck failed.')
        
        if not index_type.typecheck(df.index):
            raise TypeError('Index typecheck failed.')
        
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
        return yaml.dump({key: get_datatypes(df)}, indent=4)

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
    def __new__(cls, s: pd.Series, t: Type[S1]) -> "GenericSeries[S1]":
        def _typecheck(s: pd.Series) -> TypeGuard[GenericSeries[S1]]:
            return conv_typename(str(s.dtype)) == t.__name__
        
        if not _typecheck(s):
            raise TypeError('Typecheck failed.')
        
        return s

class TypedSeries(pd.Series, Generic[TD]):
    def __new__(cls, s: pd.Series, td: Type[TD]) -> "TypedSeries[TD]":
        def _typecheck(s: pd.Series) -> TypeGuard[TypedSeries[TD]]:
            for k, item in s.items():
                if not isinstance(item, td.__annotations__[str(k)]):
                    return False
            return True
        
        if not _typecheck(s):
            raise TypeError('Typecheck failed.')
        
        return s
