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
        self.value = value
        self.name = name
        self.__has_null: bool = self.has_null()
        self.type = self.__get_type()

    def __repr__(self):
        return 'create new column for mysql'

    def _integer(self) -> str:
        column: str = f'{self.name} {"NULL" if self.__has_null else "NOT NULL"} '
        value_to_int: list = [int(i) for i in self.value if i]
        max_val: int = max(value_to_int)

        if self._primary():
            pass
        else:
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
        column: str = f'{self.name} {"NULL" if self.__has_null else "NOT NULL"} {self.__DECIMAL[1]}'
        return column

    def _string(self) -> str:
        column = f'{self.name} '

        match self.__get_type():
            case 'char':
                column += f'CHAR({len(max(self.value))})'
            case 'varchar':
                column += f'VARCHAR(255)'
            case 'tinytext':
                column += 'TINYTEXT'
            case 'text':
                column += 'TEXT'
            case 'mediumtext':
                column += 'MEDIUMTEXT'
            case 'longtext':
                column += 'LONGTEXT'
            case _:
                raise ValueError('Incorrect string type')

        return column

    def _date(self) -> str:
        column = f'{self.name} {"NULL" if self.__has_null else "NOT NULL"} '

        match self.type:
            case 'date':
                column += self.__DATE[0]

            case 'datetime':
                column += self.__DATE[1]

            case 'timestamp':
                column += self.__DATE[2]

            case 'time':
                column += self.__DATE[3]

            case 'year':
                column += self.__DATE[4]

            case _:
                raise ValueError('Invalid date type')

        return column

    def __enum(self) -> str:
        """
        build column enum
        :return str:
        """
        values = ''
        for i in self.value:
            if i:
                values += f'{i},'
            else:
                raise ValueError('Enum value cant be null')
        del values[:-1]

        return f'{self.name} ENUM({values})'

    def _primary(self) -> bool:
        pass

    def _foreign(self) -> str:
        pass

    def __get_type(self) -> str:
        """
        get the type of column
        :return:
        """
        date = self.__is_date()

        if date[0]:
            return date[1]
        elif self.is_float():
            return 'float'
        elif self.is_str():
            return 'str'
        elif self.is_enum():
            return 'enum'
        elif self.is_foreign():
            return 'fk'
        elif self.is_primary():
            return 'pk'
        else:
            return 'int'

    def is_float(self) -> bool:
        """
        check if the value is float
        :return bool:
        """
        for i in self.value:
            if re.match(r'^[0-9]+(.|,)[0-9]+$', i, re.MULTILINE):
                return True
        return False

    def is_str(self) -> bool:
        """
        check if is str
        :return:
        """
        for i in self.value:
            if re.match(r'\D', i, re.MULTILINE):
                return True
        return False

    def is_foreign(self) -> bool:
        """
        check if col is foreign key
        :return:
        """
        if re.match(r'^fk_[aA-zZ]+$', self.name, re.MULTILINE):
            try:
                for i in self.value:
                    int(i)
            except ValueError:
                raise ValueError('Cant be foreign key string val spotted')
            return True
        return False

    def is_enum(self) -> bool:
        """
        check if enum
        :return:
        """
        if re.match(r'^enum_[aA-zZ]+$', self.name, re.MULTILINE):
            return True
        return False

    def is_primary(self) -> bool:
        """
        check if primary
        :return:
        """
        if re.match(r'^pk_[aA-zZ]+$', self.name, re.MULTILINE):
            try:
                for i in self.value:
                    int(i)
            except ValueError:
                raise ValueError('Column cant be primary key string value spotted')
            return True
        return False

    def __is_date(self) -> tuple:
        """
        check if is date
        :return:
        """
        date_format: dict = {
            "date": 0,
            "datetime": 0,
            "timestamp": 0,
            "time": 0,
            "year": 0,
        }

        # check date format
        for value in self.value:
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

        return max(date_format.values()) > len(self.value) / 2, max(date_format)

    def has_null(self) -> bool:
        """
        check if has null
        :return:
        """
        return '' in self.value

    def build(self) -> str:
        """
        build column
        :return str:
        """
        match self.type:
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
