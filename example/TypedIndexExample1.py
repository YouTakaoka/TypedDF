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
    print(TMI1(idx))

    idx2: pd.Index = df.set_index(['name', 'age', 'married']).index
    TMI2: TypedMultiIndexType[IdxType2] = TypedMultiIndexType(IdxType2)
    print(TMI2(idx2))

    TMI1_a: TypedMultiIndexType[IdxType1] = TypedMultiIndexType(IdxType2)   # OK
    TMI2_a: TypedMultiIndexType[IdxType2] = TypedMultiIndexType(IdxType1)   # Static type check fails!
    print(TMI1_a(idx))
    print(TMI2_a(idx2))

    try:
        print(TMI1(idx2)) #Runtime error!
    except TypeError as e:
        print(e)
    
    try:
        print(TMI2(idx))
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    main()
