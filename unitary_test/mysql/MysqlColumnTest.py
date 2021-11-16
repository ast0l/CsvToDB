import unittest
from csvtodb.mysql.MysqlColumn import MysqlColumn


class MysqlColumnTest(unittest.TestCase):
    column = MysqlColumn(name='', value=[])

    def is_int_test(self):
        self.column.value = ['15', '16', '17', '18']
        self.assertEqual('int', self.column.type, 'test passed')  # add assertion here

    def is_float_test(self):
        pass

    def is_str_test(self):
        pass

    def is_enum_test(self):
        pass

    def is_pk_test(self):
        pass

    def is_foreign_test(self):
        pass


if __name__ == '__main__':
    unittest.main()
