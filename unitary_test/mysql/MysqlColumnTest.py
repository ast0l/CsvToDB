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

    # tiny text
    def test_build_notnull_tinytext(self):  # change value
        column = MysqlColumn(name='col_name', value=['string', '45.00', '48'])
        result = 'col_name NOT NULL TINYTEXT'
        self.assertEqual(result, column.build())

    def test_build_null_tinytext(self):  # change value
        column = MysqlColumn(name='col_name', value=['string', 'string', 'string'])
        result = 'col_name NULL TINYTEXT'
        self.assertEqual(result, column.build())

    # medium text
    def test_build_notnull_mediumtext(self):  # change value
        column = MysqlColumn(name='col_name', value=['string', '45.00', '48'])
        result = 'col_name NOT NULL MEDIUMTEXT'
        self.assertEqual(result, column.build())

    def test_build_null_mediumtext(self):  # change value
        column = MysqlColumn(name='col_name', value=['string', 'string', 'string'])
        result = 'col_name NULL MEDIUMTEXT'
        self.assertEqual(result, column.build())

    # long text
    def test_build_notnull_longtext(self):  # change value
        column = MysqlColumn(name='col_name', value=['string', '45.00', '48'])
        result = 'col_name NOT NULL LONGTEXT'
        self.assertEqual(result, column.build())

    def test_build_null_longtext(self):  # change value
        column = MysqlColumn(name='col_name', value=['string', 'string', 'string'])
        result = 'col_name NULL LONGTEXT'
        self.assertEqual(result, column.build())

    # int
    def test_build_notnull_int(self):
        column = MysqlColumn(name='col_name', value=['45', '45', '48'])
        result = 'col_name NOT NULL UNSIGNED INT'
        self.assertEqual(result, column.build())

    def test_build_null_int(self):
        column = MysqlColumn(name='col_name', value=['45', '', '48'])
        result = 'col_name NULL UNSIGNED INT'
        self.assertEqual(result, column.build())

    def test_build_notnull_signed_int(self):
        column = MysqlColumn(name='col_name', value=['-45', '45', '48'])
        result = 'col_name NOT NULL SIGNED INT'
        self.assertEqual(result, column.build())

    def test_build_null_signed_int(self):
        column = MysqlColumn(name='col_name', value=['-45', '45', ''])
        result = 'col_name NULL SIGNED INT'
        self.assertEqual(result, column.build())

    def test_build_enum(self):
        column = MysqlColumn(name='col_name-enum', value=['small', 'medium', 'large'])
        result = 'col_name ENUM(\'small\', \'medium\', \'large\')'
        self.assertEqual(result, column.build())

    def test_build_foreign(self):
        column = MysqlColumn(name='fk_col_name-table', value=['1', '1', '1'])
        result = 'col_name INT,\n ' \
                 'INDEX col_name_ind (col_name)\n' \
                 'FOREIGN KEY (col_name)\n' \
                 '\tREFERENCES table(id)\n'
        self.assertEqual(result, column.build())

    def test_build_primary(self):
        column = MysqlColumn(name='pk_col_name', value=['1', '1', '1'])
        result = 'col_name INT PRIMARY KEY AUTOINCREMENT UNSIGNED NOT NULL'
        self.assertEqual(result, column.build())


if __name__ == '__main__':
    unittest.main()
