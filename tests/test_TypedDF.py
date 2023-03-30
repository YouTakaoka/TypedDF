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
        tdf: TypedDF[GenericIndexType[int], Human] = TypedDF(df, Human)
        self.assertTrue((tdf == df).all().all())

    def test_loading2(self):
        tdf2: TypedDF[GenericIndexType[int], Human2] = TypedDF(df2, Human2)
        self.assertTrue((tdf2 == df2).all().all())

    def test_typecheck(self):
        with self.assertRaises(TypeError):
            tdf: TypedDF[GenericIndexType[int], Human2] = TypedDF(df, Human2)

    def test_typecheck2(self):
        with self.assertRaises(TypeError):
            tdf2: TypedDF[GenericIndexType[int], Human] = TypedDF(df2, Human)

if __name__ == '__main__':
    unittest.main()
