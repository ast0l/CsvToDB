import re
from csvtodb.Column import Column


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

    def __repr__(self):
        return 'create new column for mysql'

    @classmethod
    def _integer(cls, column_value: list, column_name: str) -> str:
        column: str = column_name
        min_val = int(min(column_value))
        max_val = int(max(column_value))

        # select type
        if min_val < 0:
            for i in cls.__SIGNED:
                if (cls.__SIGNED[i][0]) <= max_val <= (cls.__SIGNED[i][1]):
                    column += f' {i.upper()} __SIGNED'
                    break
        else:
            for i in cls.__UNSIGNED:
                if (cls.__UNSIGNED[i][0]) <= max_val <= (cls.__UNSIGNED[i][1]):
                    column += f' {i.upper()} UNSIGNED'
                    break

        # check if need to add extra keywords
        if len(str(min_val)) == len(str(max_val)):
            column += ' ZEROFILL'
        else:
            column += ' NULL' if len(str(min_val)) == 0 else ' NOT NULL'

        return column

    @classmethod
    def _decimal(cls, column_value: list, column_name: str) -> str:
        column: str = column_name

        range_value = (min(column_value), max(column_value))
        range_value_str: tuple = (len(range_value[0]), len(range_value[1]))
        integer, decimal = range_value[0 if range_value_str[0] > range_value_str[1] else 1].split('.')

        zerofill: bool = True if range_value_str[0] == range_value_str[1] else False

        column += f' {cls.__DECIMAL[1]}' if len(decimal) > 2 else f' {cls.__DECIMAL[0]}'
        column += ' __SIGNED' if int(integer) < 0.0 else ' UNSIGNED'

        if zerofill:
            column += ' ZEROFILL'

        column += ' NOT NULL' if not range_value_str[0] == 0 else ' NULL'
        return column

    @classmethod
    def _string(cls, column_value: list, column_name: str, charset: str = 'utf8',
                collation: str = 'utf8_general_ci') -> str:
        column: str = column_name
        min_val = len(min(column_value, key=len))
        max_val = len(max(column_value, key=len))
        is_text: bool = False

        # for i in column_value:
        #     if re.match(r'[\n\t]', column_value[i], re.MULTILINE):
        #         is_text = True
        #         break

        # set the type
        if is_text:
            for i in cls.__STRING:
                if i != 'char' and i != 'varchar':
                    if max_val <= cls.__STRING[i]:
                        column += f' {i.upper()}({max_val})'
                        break
        else:
            column += f' {"CHAR" if min_val == max_val and max_val <= 255 else "VARCHAR"}({max_val})'
            column += f' CHARACTER SET {charset} COLLATE {collation}'

        # check if null
        column += ' NULL' if min_val == 0 else ' NOT NULL'

        return column

    @classmethod
    def _date(cls, column_value: list, column_name: str) -> str:
        column: str = column_name

        if re.match(r'^([0-9]{2}|[0-9])[-/.]([0-9]{2}|[0-9])[-/.][0-9]{4}$|^[0-9]{4}$', column_value[0], re.MULTILINE):
            column += f' {cls.__DATE[0]} NOT NULL'
        elif re.match(r'^[0-9]{4}$', column_value[0], re.MULTILINE):
            column += f' {cls.__DATE[3]} NOT NULL'
        elif re.match(r'^[0-9]{2}:[0-9]{2}:[0-9]{2}$', column_value[0], re.MULTILINE):
            column += f' {cls.__DATE[2]} NOT NULL'
        elif re.match(r'^([0-9]{2}|[0-9])([-/.][0-9]{2}|[-/.][0-9])[-/.][0-9]{4}\s[0-9]{2}:[0-9]{2}:[0-9]{2}$',
                      column_value[0], re.MULTILINE):
            timestamp: bool = True
            for i in column_value:
                val, hour = column_value[i].split(' ')
                day, month, year = val.split('/')
                hour, minute, second = hour.split(':')
                if 1970 <= int(year) <= 2038:
                    if ((int(year) == 2038 and int(day) >= 19) or (int(year) == 1970 and int(day) > 1)) and \
                            (int(month) == 1 and int(hour) == 0 and int(minute) == 0 and int(second) > 1):
                        timestamp = False
                        break
            column += f' {cls.__DATE[4 if timestamp else 1]} NOT NULL'
        return column

    @classmethod
    def _primary(cls) -> str:
        return f'\nid INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY'

    @classmethod
    def _foreign(cls, column_value: list, column_name: str) -> str:
        """
        build foreign key for mysql
        :return:
        """
        table, field = column_name.split('_')
        column = column_name

        for i in cls.__UNSIGNED:
            if i == 'int' or i == 'bigint' and (cls.__UNSIGNED[i][0]) <= int(max(column_value)) <= (cls.__UNSIGNED[i][1]):
                column += f' {i.upper()} UNSIGNED NOT NULL,\n'
                break

        column += f'INDEX ix_{table}({column_name}),\n'
        column += f'FOREIGN KEY ({column_name})' \
                  f'\n\tREFERENCES {table}({field})' \
                  f'\n\tON DELETE {cls.__FOREIGN_REFERENCES[1]}' \
                  f'\n\tON UPDATE {cls.__FOREIGN_REFERENCES[1]}'

        return column
