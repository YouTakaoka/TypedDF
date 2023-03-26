from TypedDF import *

class TMI1(TypedDict):
    name: str
    age: int

class TMI2(TypedDict):
    name: str
    age: int
    married: bool

def main():
    df: pd.DataFrame = pd.read_csv('example/human_list.csv')
    idx: pd.Index = df.set_index(['name', 'age']).index
    tmi: TypedMultiIndex[TMI1] = TypedMultiIndex.from_index(idx, TMI1)
    print(tmi)

    idx2: pd.Index = df.set_index(['name', 'age', 'married']).index
    tmi2: TypedMultiIndex[TMI2] = TypedMultiIndex.from_index(idx2, TMI2)
    print(tmi2)

    tmi_a: TypedMultiIndex[TMI2] = tmi    # Static type check fails!
    tmi2_a: TypedMultiIndex[TMI1] = tmi2  # Static type check fails!
    print(tmi_a)
    print(tmi2_a)

    try:
        tdf3: TypedMultiIndex[TMI1] = TypedMultiIndex.from_index(idx2, TMI1) #Runtime error!
        print(tdf3)
    except TypeError as e:
        print(e)
    
    try:
        tdf4: TypedMultiIndex[TMI2] = TypedMultiIndex.from_index(idx, TMI2) #Runtime error!
        print(tdf4)
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    main()
