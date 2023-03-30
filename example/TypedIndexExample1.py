from TypedDF import *

class IdxType1(TypedDict):
    name: str
    age: int

class IdxType2(TypedDict):
    name: str
    age: int
    married: bool

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    idx: pd.Index = df.set_index(['name', 'age']).index
    TMI1: TypedMultiIndexType[IdxType1] = TypedMultiIndexType(IdxType1)
    print(TypedIndex(idx, TMI1))

    idx2: pd.Index = df.set_index(['name', 'age', 'married']).index
    TMI2: TypedMultiIndexType[IdxType2] = TypedMultiIndexType(IdxType2)
    print(TypedIndex(idx2, TMI2))

    TMI1_a: TypedMultiIndexType[IdxType2] = TypedMultiIndexType(IdxType1)  # Static type check fails!
    TMI2_a: TypedMultiIndexType[IdxType1] = TypedMultiIndexType(IdxType2)  # OK
    print(TypedIndex(idx, TMI1_a))
    print(TypedIndex(idx2, TMI2_a))

    try:
        print(TypedIndex(idx2, TMI1)) #Runtime error!
    except TypeError as e:
        print(e)
    
    try:
        print(TypedIndex(idx, TMI2)) #Runtime error!
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    main()
