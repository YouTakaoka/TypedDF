from typeddf.TypedDF import *
from example.Human import Human
from example.Human2 import Human2

class Human(TypedDict):
    height: float
    married: bool

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    df.set_index(['name', 'age'], inplace=True)

    tdf: TypedDF[Human, str, int] = TypedDF(df, Human, T_STR, T_INT)  # OK
    print(tdf)

if __name__ == '__main__':
    main()
