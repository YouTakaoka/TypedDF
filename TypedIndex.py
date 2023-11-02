from typing import TypeGuard
import pandas as pd

from _types import *

T_STR = ""
T_INT = 0
T_BOOL = True

T_LIT = Literal["", 0, True]

_TYPE_DICT: dict[T_LIT, SCALAR_NAME] = {
    T_STR: "str",
    T_INT: "int",
    T_BOOL: "bool",
}

def _get_typename(t) -> SCALAR_NAME:
    assert t in _TYPE_DICT.keys()
    return _TYPE_DICT[t]

class TypedIndex(pd.Index, Generic[IDX]):
    def __new__(cls, idx: pd.Index, index_type: IDX) -> Self:
        if not cls.typecheck(idx, index_type):
            raise TypeError("Index typecheck failed.")
        return idx

    @classmethod
    def typecheck(cls, idx: pd.Index, index_type: IDX) -> TypeGuard[Self]:
        if isinstance(index_type, )

        get_datatypes(idx.to_frame())
        tn: list[SCALAR_NAME] = [conv_typename(str(t)) for t in idx.to_frame().dtypes]
        return tn == [_get_typename(t) for t in index_type]
