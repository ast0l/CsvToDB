import re
from generic.Column import Column


class MysqlColumn(Column):
    __FOREIGN_REFERENCES: tuple = ('RESTRICT', 'CASCADE', 'NO ACTION', 'SET DEFAULT', 'SET NULL')  # on_update/on_delete
    __SIGNED: dict = {
        'tinyint': (-128, 127),
        'smallint': (-32768, 32767),
        'mediumint': (-8388608, 8388607),
        'int': (-2147483648, 2147483647),
        'bigint': (-2 ** 63, 2 ** 63 - 1),
    }  # signed type name: value
    __UNSIGNED: dict = {
        'tinyint': (0, 255),
        'smallint': (0, 65535),
        'mediumint': (0, 16777215),
        'int': (0, 4294967295),
        'bigint': (0, 2 ** 64 - 1),
    }  # unsigned type name: value
    __STRING: dict = {
        'char': 255,
        'varchar': 65.535,
        'tinytext': 2 ** 8,
        'text': 2 ** 16,
        'mediumtext': 2 ** 24,
        'longtext': 2 ** 32,
    }  # string type name: value
    __DATE: tuple = ('DATE', 'DATETIME', 'TIME', 'YEAR', 'TIMESTAMP')  # date type name
    __DECIMAL: tuple = ('FLOAT', 'DOUBLE')

    def __init__(self, name: str, value: list):
        super().__init__(name, value)
        self.unsigned: bool = True

    def __repr__(self):
        return 'create new column for mysql'

    def _integer(self) -> str:
        pass

    def _decimal(self) -> str:
        pass

    def _string(self) -> str:
        pass

    def _date(self) -> str:
        pass

    def _primary(self) -> str:
        pass

    def _foreign(self) -> str:
        pass

    def get_type(self):
        # check if column is string or numeric value
        try:
            for value in self._value:
                i = self._value.index(value)
                value = int(value)
                self._value[i] = value

                if self.unsigned and value < 0:
                    self.unsigned = False

            print('is int')
        except ValueError:  # if value cant be transform into an int specified it to str
            print('is string')