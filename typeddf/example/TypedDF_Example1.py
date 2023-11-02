from typeddf.TypedDF import *

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    TypedDF.save_classdef(df, 'Human', file_name='example/Human.py')

    df2: pd.DataFrame = pd.read_csv('example/human_list2.csv')
    TypedDF.save_classdef(df2, 'Human2', file_name='example/Human2.py')

if __name__ == '__main__':
    main()
