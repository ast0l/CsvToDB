import re
from csvtodb.generic.Column import Column


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
    __DATE: tuple = ('DATE', 'DATETIME', 'TIMESTAMP', 'TIME', 'YEAR')  # date type name
    __DECIMAL: tuple = ('FLOAT', 'DOUBLE')

    def __init__(self, name: str, value: list):
        super().__init__(name, value)
        self.__has_null: bool = False
        self.__type = self.__get_type()

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
        column: str = f'{self._name} {"NULL" if self.__has_null else "NOT NULL"} {self.__DECIMAL[1]}'
        return column

    def _string(self) -> str:
        column = f'{self._name} {"NULL" if self.__has_null else "NOT NULL"} '
        larger_value = max(self._value)

        for i in self._value:
            i = len(i)
            if i < len(larger_value) or i > len(larger_value):
                column += 'VARCHAR(255)'
                return column

        column += f'CHAR({len(larger_value)})'
        return column

    def _date(self, date_type: str | None = None) -> str:
        column = f'{self._name} {"NULL" if self.__has_null else "NOT NULL"} '

        match date_type:
            case 'date':
                column += self.__DATE[0]

            case 'datetime':
                column += self.__DATE[1]

            case 'timestamp':
                column += self.__DATE[2]

            case _:
                raise ValueError('Invalid date type')

        return column

    def _primary(self) -> bool:
        pass

    def _foreign(self) -> str:
        pass

    def __get_type(self) -> str:
        """
        get the type of column
        :return:
        """
        is_str: bool = False

        # check if numeric decimal or string value
        for value in self._value:
            if value:
                try:
                    # check if can be int or float
                    int(value)
                    if re.match(r'^[0-9]+(.|,)[0-9]+$', value, re.MULTILINE):
                        return 'float'
                except ValueError:
                    # check if simple string or date format
                    is_str = True
                    break
            else:
                self.__has_null = True

        # check is the string can be date
        if is_str:
            date_format: dict = {
                "date": 0,
                "datetime": 0,
                "timestamp": 0,
                "time": 0,
                "year": 0,
            }

            for value in self._value:
                # date
                if re.match(r'^[0-9]{4}-|/[0-9]{2}-|/[0-9]{2}$', value, re.MULTILINE):
                    date_format["date"] += 1

                # datetime
                elif re.match(r'^[0-9]{4}-|/[0-9]{2}-|/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', value, re.MULTILINE):
                    date_format["datetime"] += 1

                # timestamp
                elif re.match(r'^[0-9]{4}-|/[0-9]{2}-|/[0-9]{2}$', value, re.MULTILINE):
                    date_format["timestamp"] += 1

                # time
                elif re.match(r'^[0-9]{2}:[0-9]{2}:[0-9]{2}$', value, re.MULTILINE):
                    date_format["time"] += 1

            recurrent_format = max(date_format.values())

            # if the most reccurent format is less than 50% of the total value in the row
            # consider it like string and not date
            if recurrent_format == 0 or recurrent_format < len(self._value)/2:
                return 'str'
            else:
                return max(date_format)

        return 'int'

    def build(self) -> str:
        """
        build column
        :return str:
        """
        match self.__type:
            case 'int':
                return self._integer()

            case 'float':
                return self._decimal()

            case 'str':
                return self._string()

            case 'date', 'datetime', 'timestamp':
                return self._date()

            case _:
                raise ValueError('Can\'t build column no type specified')
