from typing import TypeGuard
import pandas as pd

from _types import *

class IndexType:
    def typecheck(self, idx: pd.Index) -> "TypeGuard[TypedIndex]":
        ...

class GenericIndexType(IndexType, Generic[H]):
    def __init__(self, t: Type[H]) -> None:
        self.t = t

    def typecheck(self, idx: pd.Index) -> "TypeGuard[TypedIndex[GenericIndexType[H]]]":
        return conv_typename(str(idx.dtype)) == self.t.__name__

class TypedMultiIndexType(IndexType):
    def __init__(self, *ts: Type[Hashable]) -> None:
        self.ts: list[str] = [t.__name__ for t in ts]

    def typecheck(self, idx: pd.Index) -> "TypeGuard[TypedIndex[TypedMultiIndexType]]":
        ts: list[SCALAR_NAME] = [conv_typename(str(t)) for t in idx.to_frame().dtypes]
        return self.ts == ts

GIT_INT: GenericIndexType[int] = GenericIndexType(int)

IDX = TypeVar('IDX', bound = IndexType)

class TypedIndex(pd.Index, Generic[IDX]):
    def __new__(cls, idx: pd.Index, index_type: IDX) -> "TypedIndex[IDX]":
        if not index_type.typecheck(idx):
            raise TypeError('Index typecheck failed.')
       
        return idx
