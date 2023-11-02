from typeddf.TypedDF import *

def main() -> None:
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    print(df)

    idx: pd.Index = df.set_index(['name', 'age']).index
    TI1: TypedIndex[str, int] = TypedIndex(idx, T_STR, T_INT)
    print(TI1)

    idx2: pd.Index = df.set_index(['name', 'age', 'married']).index
    TI2 = TypedIndex(idx2, T_STR, T_INT, T_BOOL)
    print(TI2)

    try:
        print(TypedIndex(idx2, T_STR, T_INT)) #Runtime error!
    except TypeError as e:
        print(e)
    
    try:
        print(TypedIndex(idx, T_STR, T_INT, T_BOOL)) #Runtime error!
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    main()
