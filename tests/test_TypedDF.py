import unittest
from TypedDF import *
from example.Human import Human
from example.Human2 import Human2

data = [
        {'name': 'Taro', 'age': 7, 'married': False, 'height': 174.48},
        {'name': 'Hanako', 'age': 3, 'married': True, 'height': 152.60}
    ]
df = pd.DataFrame(data)
df2: pd.DataFrame = df.copy()
df2['comment'] = ["I'll be back!", ""]

class TestTypedDF(unittest.TestCase):
    def test_loading(self):
        tdf: TypedDF[Human] = TypedDF.from_df(Human, df)
        self.assertTrue((tdf == df).all().all())

    def test_loading2(self):
        tdf2: TypedDF[Human2] = TypedDF.from_df(Human2, df2)
        self.assertTrue((tdf2 == df2).all().all())

    def test_typecheck(self):
        with self.assertRaises(TypeError):
            tdf: TypedDF[Human2] = TypedDF.from_df(Human2, df)

    def test_typecheck2(self):
        with self.assertRaises(TypeError):
            tdf2: TypedDF[Human] = TypedDF.from_df(Human, df2)

if __name__ == '__main__':
    unittest.main()
