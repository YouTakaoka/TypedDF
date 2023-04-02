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
    TMI1 = TypedMultiIndexType(str, int)
    print(TypedIndex(idx, TMI1))

    idx2: pd.Index = df.set_index(['name', 'age', 'married']).index
    TMI2 = TypedMultiIndexType(str, int, bool)
    print(TypedIndex(idx2, TMI2))

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
