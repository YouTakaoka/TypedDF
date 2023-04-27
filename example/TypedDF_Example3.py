from TypedDF import *
from example.Human import Human
from example.Human2 import Human2

class Human(TypedDict):
    height: float
    married: bool

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    df.set_index(['name', 'age'], inplace=True)

    TMI1 = TypedMultiIndexType(str, int)
    tdf: TypedDF[TypedMultiIndexType, Human] = TypedDF(df, Human, index_type = TMI1)  # OK
    print(tdf)

if __name__ == '__main__':
    main()
