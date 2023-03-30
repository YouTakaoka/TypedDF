from TypedDF import *
from example.Human import Human
from example.Human2 import Human2

class IdxType1(TypedDict):
    name: str
    age: int

TMI1: TypedMultiIndexType[IdxType1] = TypedMultiIndexType(IdxType1)
GIT: GenericIndexType[int] = GenericIndexType(int)

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    tdf: TypedDF[GenericIndexType[int], Human] = TypedDF.from_df(df, Human, IndexType(GIT))  # OK
    print(tdf)

    df2: pd.DataFrame = pd.read_csv('example/human_list2.csv')
    tdf2: TypedDF[GenericIndexType[int], Human2] = TypedDF.from_df(df2, Human2, IndexType(GIT)) # OK
    print(tdf2)

    tdf_a: TypedDF[GenericIndexType[int], Human2] = tdf   # Static type check fails!
    tdf2_a: TypedDF[GenericIndexType[int], Human] = tdf2  # Static type check fails!
    print(tdf_a)
    print(tdf2_a)

    try:
        tdf3: TypedDF[GenericIndexType[int], Human2] = TypedDF.from_df(df, Human2, IndexType(GIT)) #Runtime error!
        print(tdf3)
    except TypeError as e:
        print(e)
    
    try:
        tdf4: TypedDF[GenericIndexType[int], Human] = TypedDF.from_df(df2, Human, IndexType(GIT)) #Runtime error!
        print(tdf4)
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    main()
