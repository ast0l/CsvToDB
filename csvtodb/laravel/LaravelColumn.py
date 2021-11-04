import re
from generic.Column import Column


class LaravelColumn(Column):
    __FOREIGN_REFERENCES: tuple = ('restrict', 'cascade', 'no action', 'set default', 'set null')  # on_update/on_delete
    __SIGNED: dict = {
        'tinyInteger': (-128, 127),
        'smallInteger': (-32768, 32767),
        'mediumInteger': (-8388608, 8388607),
        'integer': (-2147483648, 2147483647),
        'bigInteger': (-2 ** 63, 2 ** 63 - 1),
    }  # signed type name: value
    __UNSIGNED: dict = {
        'unsignedTinyInteger': (0, 255),
        'unsignedSmallInteger': (0, 65535),
        'unsignedMediumInteger': (0, 16777215),
        'unsignedInteger': (0, 4294967295),
        'unsignedBigInteger': (0, 2 ** 64 - 1),
    }  # unsigned type name: value
    __STRING: dict = {
        'char': 255,
        'string': 65.535
    }  # string type name: value
    __TEXT: dict = {
        'tinyText': 2 ** 8,
        'text': 2 ** 16,
        'mediumText': 2 ** 24,
        'longText': 2 ** 32
    }  # text type name: value
    __DATE: tuple = ('date', 'datetime', 'time', 'year', 'timestamp')  # date type name
    __DECIMAL: tuple = ('float', 'double')  # decimal type name

    def __repr__(self):
        return 'build column for laravel'

    @classmethod
    def _integer(cls, column_value: list, column_name: str) -> str:
        column: str = '\t\t\t$table->'
        min_val = int(min(column_value))
        max_val = int(max(column_value))

        # select type
        if min_val < 0:
            for i in cls.__SIGNED:
                if (cls.__SIGNED[i][0]) <= max_val <= (cls.__SIGNED[i][1]):
                    column += f'{i}("{column_name}")'
                    break
        else:
            for i in cls.__UNSIGNED:
                if (cls.__UNSIGNED[i][0]) <= max_val <= (cls.__UNSIGNED[i][1]):
                    column += f'{i}("{column_name}")'
                    break

        # check if need to add extra keywords
        if len(str(min_val)) == 0:
            column += '->nullable()'
        column += ';\n'
        return column

    @classmethod
    def _decimal(cls, column_value: list, column_name: str) -> str:
        column: str = '\t\t\t$table->'

        range_value = (min(column_value), max(column_value))
        range_value_str: tuple = (len(re.sub(r'\D+', '', range_value[0], 0, re.MULTILINE)),
                                  len(re.sub(r'\D+', '', range_value[1], 0, re.MULTILINE)))
        integer, decimal = range_value[range_value_str.index(max(range_value_str))].split('.')

        if int(integer) < 0.000:
            column += f'{cls.__DECIMAL[1 if len(decimal) > 2 else 0]}->("{column_name}")'
        else:
            total = len(integer) + len(decimal)
            column += f'unsignedDecimal("{column_name}", {total}, {len(decimal)})'

        if range_value_str[0] == 0:
            column += '->nullable()'
        column += ';\n'
        return column

    @classmethod
    def _string(cls, column_value: list, column_name: str, charset: str = 'utf8',
                collation: str = 'utf8_general_ci') -> str:
        column: str = '\t\t\t$table->'
        min_val = len(min(column_value, key=len))
        max_val = len(max(column_value, key=len))
        is_text: bool = False

        for i in column_value:
            if re.match(r'[\n\t]', column_value[column_value.index(i)], re.MULTILINE):
                is_text = True
                break

        # set the type
        if is_text:
            for i in cls.__TEXT:
                if max_val <= cls.__TEXT[i]:
                    column += f' {i}({max_val})'
                    break
        else:
            column += f'{"char" if min_val == max_val and max_val <= cls.__STRING["char"] else "string"}("{column_name}", {max_val})'

        # check if null
        if min_val == 0:
            column += '->nullable()'

        column += f'->charset("{charset}")->collation("{collation}")'
        column += ';\n'
        return column

    @classmethod
    def _date(cls, column_value: list, column_name: str) -> str:
        column: str = '\t\t\t$table->'

        if re.match(r'^([0-9]{2}|[0-9])[-/.]([0-9]{2}|[0-9])[-/.][0-9]{4}$|^[0-9]{4}$', column_value[0], re.MULTILINE):
            column += f'{cls.__DATE[0]}("{column_name}")'
        elif re.match(r'^[0-9]{4}$', column_value[0], re.MULTILINE):
            column += f'{cls.__DATE[3]}("{column_name}")'
        elif re.match(r'^[0-9]{2}:[0-9]{2}:[0-9]{2}$', column_value[0], re.MULTILINE):
            column += f'{cls.__DATE[2]}("{column_name}")'
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
            column += f' {cls.__DATE[4 if timestamp else 1]}("{column_name}")'
            column += '->useCurrentOnUpdate()'
            column += '->useCurrent()'

        column += ';\n'
        return column

    @classmethod
    def _primary(cls) -> str:
        return f'\n\t\t\t$table->id();\n'

    @classmethod
    def _foreign(cls, column_value: list, column_name: str) -> str:
        """
        build foreign key for mysql
        :return:
        """
        table, field = column_name.split('_')
        column = f'\n\t\t\t$table->foreignId("{column_name}")' \
                 f'->constrained("{table}")' \
                 f'->onUpdate("{cls.__FOREIGN_REFERENCES[1]}")' \
                 f'->onDelete("{cls.__FOREIGN_REFERENCES[1]}");\n'

        return column
