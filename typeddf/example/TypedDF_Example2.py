from typeddf.TypedDF import *
from example.Human import Human
from example.Human2 import Human2

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    tdf: TypedDF[Human, int] = TypedDF(df, Human, T_INT)  # OK
    print(tdf)

    df2: pd.DataFrame = pd.read_csv('example/human_list2.csv')
    tdf2: TypedDF[Human2, int] = TypedDF(df2, Human2, T_INT) # OK
    print(tdf2)

    tdf_a: TypedDF[Human2, int] = TypedDF(df, Human, T_INT)    # Static type check fails!
    tdf2_a: TypedDF[Human, int] = TypedDF(df2, Human2, T_INT)  # Static type check fails!
    print(tdf_a)
    print(tdf2_a)

    try:
        tdf3: TypedDF[Human2, int] = TypedDF(df, Human2, T_INT) #Runtime error!
        print(tdf3)
    except TypeError as e:
        print(e)
    
    try:
        tdf4: TypedDF[Human, int] = TypedDF(df2, Human, T_INT) #Runtime error!
        print(tdf4)
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    main()
