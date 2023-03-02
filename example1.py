from TypedDF import *

df: pd.DataFrame = pd.read_csv('human_list.csv')
save_classdef(df, 'Human2')
