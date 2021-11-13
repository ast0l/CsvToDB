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
        self.__type = self.__get_type()
        self.__has_null: bool = False

    def __repr__(self):
        return 'create new column for mysql'

    def _integer(self) -> str:
        column: str = f'{self._name} {"NULL" if self.__has_null else "NOT NULL"} '
        value_to_int: list = [int(i) for i in self._value if i]
        max_val: int = max(value_to_int)

        if min(value_to_int) < 0:
            for unsigned_val in self.__UNSIGNED:
                if not max_val > self.__UNSIGNED[unsigned_val][1]:
                    column += f'{unsigned_val.upper()}({self.__UNSIGNED[unsigned_val][1]}) UNSIGNED'
                    break
        else:
            for signed_val in self.__SIGNED:
                if self.__SIGNED[signed_val][0] < max_val > self.__SIGNED[signed_val][1]:
                    column += f'{signed_val.upper()}({self.__SIGNED[signed_val][1]}) SIGNED'
                    break

        return column

    def _decimal(self) -> str:
        pass

    def _string(self) -> str:
        pass

    def _date(self) -> str:
        pass

    def _primary(self) -> bool:
        pass

    def _foreign(self) -> str:
        pass

    def __get_type(self) -> str | float | int:
        """
        get the type of column
        :return:
        """
        # check if numeric decimal or string value
        for value in self._value:

            if value:
                try:
                    int(value)
                    if re.match(r'^[0-9]+(.|,)[0-9]+$', value, re.MULTILINE):
                        return float()
                except ValueError:
                    return str()
            else:
                self.__has_null = True

        return int()

    def build(self) -> str:
        """
        build column
        :return str:
        """
        if isinstance(self.__type, str):
            return self._string()

        elif isinstance(self.__type, int):
            print('int')
            return self._integer()

        elif isinstance(self.__type, float):
            return self._decimal()
