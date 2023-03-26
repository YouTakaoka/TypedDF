from TypedDF import *
from example.Human import Human
from example.Human2 import Human2

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    tdf: TypedDF[Human] = TypedDF.from_df(Human, df)    # OK
    print(tdf)

    df2: pd.DataFrame = pd.read_csv('example/human_list2.csv')
    tdf2: TypedDF[Human2] = TypedDF.from_df(Human2, df2) # OK
    print(tdf2)

    tdf_a: TypedDF[Human2] = tdf   # Static type check fails!
    tdf_2a: TypedDF[Human] = tdf2  # Static type check fails!
    print(tdf_a)
    print(tdf_2a)

    try:
        tdf3: TypedDF[Human2] = TypedDF.from_df(Human2, df) #Runtime error!
        print(tdf3)
    except TypeError as e:
        print(e)
    
    try:
        tdf4: TypedDF[Human] = TypedDF.from_df(Human, df2) #Runtime error!
        print(tdf4)
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    main()
