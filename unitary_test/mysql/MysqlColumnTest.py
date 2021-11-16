import unittest
from csvtodb.mysql.MysqlColumn import MysqlColumn


class MysqlColumnTest(unittest.TestCase):

    """
    ================================================
    test method to check type
    ================================================
    """
    def test_is_int(self):
        column = MysqlColumn(name='', value=['15', '16', '17', '18'])
        self.assertEqual('int', column.type, 'test passed')  # add assertion here

    def test_is_float(self):
        column = MysqlColumn(name='', value=['15.23', '12,25', '45', '25'])
        self.assertTrue(column.is_float())

    def test_is_str(self):
        column = MysqlColumn(name='', value=['45', '45.56', 'some text', 'test45'])
        self.assertTrue(column.is_str())

    def test_is_enum(self):
        column = MysqlColumn(name='enum_test', value=[])
        self.assertTrue(column.is_enum())

    def test_is_pk(self):
        column = MysqlColumn(name='pk_test', value=[])
        self.assertTrue(column.is_primary())

    def test_is_foreign(self):
        column = MysqlColumn(name='fk_name', value=[])
        self.assertTrue(column.is_foreign())

    def test_has_null(self):
        column = MysqlColumn(name='', value=['45', '', '50', '45y'])
        self.assertTrue(column.has_null())

    """
    ================================================
    test type set for column
    ================================================
    """
    def test_type_is_float(self):
        column = MysqlColumn(name='', value=['45.25', '', '50,52', '54'])
        self.assertEqual('float', column.type)

    def test_type_is_enum(self):
        column = MysqlColumn(name='enum_name', value=[])
        self.assertEqual('enum', column.type)

    def test_type_is_int(self):
        column = MysqlColumn(name='', value=['45', '54', '58'])
        self.assertEqual('int', column.type)

    def test_type_is_str(self):
        column = MysqlColumn(name='', value=['stre', '45', ''])
        self.assertEqual('str', column.type)

    def test_type_is_pk(self):
        column = MysqlColumn(name='pk_name', value=[])
        self.assertEqual('pk', column.type)

    def test_type_is_fk(self):
        column = MysqlColumn(name='fk_name', value=[])
        self.assertEqual('fk', column.type)


if __name__ == '__main__':
    unittest.main()
