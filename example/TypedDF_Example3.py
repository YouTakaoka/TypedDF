from TypedDF import *
from example.Human import Human
from example.Human2 import Human2

class IdxType1(TypedDict):
    name: str
    age: int

class Human(TypedDict):
    height: float
    married: bool

TMI1: TypedMultiIndexType[IdxType1] = TypedMultiIndexType(IdxType1)

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv').set_index(['name', 'age'])
    tdf: TypedDF[TypedMultiIndexType[IdxType1], Human] = TypedDF.from_df(df, Human, index_type = TMI1)  # OK
    print(tdf)

if __name__ == '__main__':
    main()
