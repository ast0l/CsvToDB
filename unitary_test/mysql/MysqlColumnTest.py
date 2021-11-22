import unittest
from csvtodb.mysql.MysqlColumn import MysqlColumn


class MysqlColumnTest(unittest.TestCase):

    """
    ================================================
    test method to check type
    ================================================
    """
    def test_has_null(self):
        column = MysqlColumn(name='', value=['45', '', '50', '45y'])
        self.assertTrue(column.has_null())

    """
    ================================================
    test build return for each type
    ================================================
    """
    def test_build_notnull_float(self):
        column = MysqlColumn(name='col_name', value=[])
        expected = 'col_name NOT NULL FLOAT'
        self.assertEqual(expected, column.build())

    def test_build_null_float(self):
        column = MysqlColumn(name='col_name', value=[])
        expected = 'col_name NOT NULL FLOAT'
        self.assertEqual(expected, column.build())

    def test_build_str(self):
        pass

    def test_build_int(self):
        pass

    def test_build_enum(self):
        pass

    def test_build_foreign(self):
        pass

    def test_build_primary(self):
        pass

if __name__ == '__main__':
    unittest.main()
