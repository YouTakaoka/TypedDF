from TypedDF import *
from Human import Human
from Human2 import Human2

df: pd.DataFrame = pd.read_csv('human_list.csv')
tdf: TypedDF[Human2] = from_df(Human2, df)
tdf2: TypedDF[Human] = from_df(Human2, df) #OK
print(tdf)
print(tdf2)

tdf3: TypedDF[Human2] = tdf2 #Static type check fails!
print(tdf3)

tdf4: TypedDF[Human] = from_df(Human, df) #Runtime error!
