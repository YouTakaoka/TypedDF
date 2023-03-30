from typing import Generic, TypeGuard, Type, NewType
import pandas as pd

from _types import *

class GenericIndexType(Generic[H]):
    def __init__(self, t: Type[H]) -> None:
        self.t = t        

class GenericIndex(pd.Index, Generic[H]):
    pass

class TypedMultiIndexType(Generic[TD]):
    def __init__(self, td: Type[TD]) -> None:
        self.td = td

class TypedMultiIndex(pd.MultiIndex, Generic[TD]):
    pass

IDX = TypeVar('IDX', bound = GenericIndexType | TypedMultiIndexType)

class IndexType(Generic[IDX]):
    def __init__(self, idx_type: IDX) -> None:
        self.idx_type = idx_type

    def typecheck(self, idx: pd.Index) -> "TypeGuard[IndexType[IDX]]":
        if isinstance(self.idx_type, GenericIndexType):             
            return conv_typename(str(idx.dtype)) == self.idx_type.t.__name__

        def _get_datatypes(idx: pd.Index) -> dict[str, Type]:
            return {str(k): conv_typename(str(t)) for k, t in idx.to_frame().dtypes.to_dict().items()}
        
        dt: dict[str, str] = {k: v.__name__ for k, v in self.idx_type.td.__annotations__.items()}
        return _get_datatypes(idx) == dt

    def __call__(self, idx: pd.Index) -> "IndexType[IDX]":
        if not self.typecheck(idx):
            raise TypeError('Typecheck failed.')
        
        return idx