from typing import Generic, TypeGuard, Type, NewType
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
    
    def __call__(self, idx: pd.Index) -> "TypedIndex[GenericIndexType[H]]":
        if not self.typecheck(idx):
            raise TypeError('Typecheck failed.')
        
        return idx

class TypedMultiIndexType(IndexType, Generic[TD]):
    def __init__(self, td: Type[TD]) -> None:
        self.td = td

    def typecheck(self, idx: pd.Index) -> "TypeGuard[TypedIndex[TypedMultiIndexType[TD]]]":
        def _get_datatypes(idx: pd.Index) -> dict[str, Type]:
            return {str(k): conv_typename(str(t)) for k, t in idx.to_frame().dtypes.to_dict().items()}
        
        dt: dict[str, str] = {k: v.__name__ for k, v in self.td.__annotations__.items()}
        return _get_datatypes(idx) == dt

    def __call__(self, idx: pd.Index) -> "TypedIndex[TypedMultiIndexType[TD]]":
        if not self.typecheck(idx):
            raise TypeError('Typecheck failed.')
        
        return idx

GIT_INT: GenericIndexType[int] = GenericIndexType(int)

IDX = TypeVar('IDX', bound = IndexType)

class TypedIndex(pd.Index, Generic[IDX]):
    def __new__(cls, idx: pd.Index, index_type: IDX) -> "TypedIndex[IDX]":
        if not index_type.typecheck(idx):
            raise TypeError('Index typecheck failed.')
       
        return idx
