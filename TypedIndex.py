from typing import Generic, TypeGuard, Type, NewType
import pandas as pd

from _types import *

class GenericIndexType(Generic[H]):
    def __init__(self, t: Type[H]) -> None:
        self.t = t

    def typecheck(self, idx: pd.Index) -> "TypeGuard[GenericIndexType[H]]":
        return conv_typename(str(idx.dtype)) == self.t.__name__
    
    def __call__(self, idx: pd.Index) -> "GenericIndexType[H]":
        if not self.typecheck(idx):
            raise TypeError('Typecheck failed.')
        
        return idx

class GenericIndex(pd.Index, Generic[H]):
    pass

class TypedMultiIndexType(Generic[TD]):
    def __init__(self, td: Type[TD]) -> None:
        self.td = td

    def typecheck(self, idx: pd.Index) -> "TypeGuard[TypedMultiIndexType[TD]]":
        def _get_datatypes(idx: pd.Index) -> dict[str, Type]:
            return {str(k): conv_typename(str(t)) for k, t in idx.to_frame().dtypes.to_dict().items()}
        
        dt: dict[str, str] = {k: v.__name__ for k, v in self.td.__annotations__.items()}
        return _get_datatypes(idx) == dt

    def __call__(self, idx: pd.Index) -> "TypedMultiIndexType[TD]":
        if not self.typecheck(idx):
            raise TypeError('Typecheck failed.')
        
        return idx

class TypedMultiIndex(pd.MultiIndex, Generic[TD]):
    pass

GIT_INT: GenericIndexType[int] = GenericIndexType(int)

IDX = TypeVar('IDX', GenericIndexType, GenericIndexType[int], TypedMultiIndexType)
