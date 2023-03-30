from TypedDF import *

GIT: GenericIndexType[int] = GenericIndexType(int)
idx: TypedIndex[GenericIndexType[int]] = TypedIndex(pd.Index([1,2,3]), GIT)
print(idx)

