import re
from csvtodb.Table import Table
from csvtodb.MysqlColumn import MysqlColumn
from csvtodb.Csv import Csv


class MysqlTable(Table, MysqlColumn):
    __ENGINE: tuple = ('innodb', 'myisam', 'memory', 'csv')

    def __repr__(self):
        return 'class to build sql table for mysql'

    @classmethod
    def _build_table(cls, csv: Csv, engine: str, temporary: bool) -> str:
        res: dict = {}
        columns: dict = cls._define_col_type(csv)
        if engine.lower() in cls.__ENGINE:
            for column in columns:
                if columns[column]:
                    if column == 'integer':
                        for i in columns[column]:
                            content: list = csv.column_content(column=i+1)
                            name: str = content.pop(0)
                            res[i] = f'{cls._integer(column_value=content, column_name=name)},\n'
                    elif column == 'decimal':
                        for i in columns[column]:
                            content: list = csv.column_content(column=i+1)
                            name: str = content.pop(0)
                            res[i] = f'{cls._decimal(column_value=content, column_name=name)},\n'
                    elif column == 'string':
                        for i in columns[column]:
                            content: list = csv.column_content(column=i+1)
                            name: str = content.pop(0)
                            res[i] = f'{cls._string(column_value=content, column_name=name)},\n'
                    elif column == 'date':
                        for i in columns[column]:
                            content: list = csv.column_content(column=i+1)
                            name: str = content.pop(0)
                            res[i] = f'{cls._date(column_value=content, column_name=name)},\n'
                    elif column == 'foreign':
                        for i in columns[column]:
                            content: list = csv.column_content(column=i+1)
                            name: str = content.pop(0)
                            res[i] = f'{cls._foreign(column_value=content, column_name=name)},\n'

            new_table: str = f'CREATE {"TEMPORARY" if temporary else ""} TABLE IF NOT EXISTS {csv.p_filename}('
            new_table += f'\t{cls._primary()},\n'
            res[max(res)] = res[max(res)][0:-2]+'\n'
            for i in range(0, len(res)):
                new_table += res[i]
            new_table += f')ENGINE="{engine.upper()}";\n\n'
            return new_table
        else:
            raise ValueError(f'engine not supported')

    @classmethod
    def _define_col_type(cls, csv: Csv) -> dict:
        """
        define column type

        :param csv:
        :return:
        """
        date_pattern: str = r'^([0-9]{2}|[0-9]{1})([-|\/|.][0-9]{2}|[-|\/|.][0-9]{1})[-|\/|.][0-9]{4}\s[0-9]{2}\:[0-9]{2}\:[0-9]{2}$|' \
                            r'^([0-9]{2}|[0-9]{1})[-|\/|.]([0-9]{2}|[0-9]{1})[-|\/|.][0-9]{4}$|^[0-9]{4}$|' \
                            r'^[0-9]{2}\:[0-9]{2}\:[0-9]{2}$'

        content: list = csv.row_list(limit=1)[0]
        col_name: tuple = csv.column_name()
        col_type: dict = {
            'integer': [],
            'decimal': [],
            'string': [],
            'date': [],
            'foreign': []
        }

        # check which col is str or numeric
        for i in range(0, len(col_name)):
            if re.search(r'_id$', col_name[i]):
                col_type['foreign'].append(i)

        for i in range(0, len(content)):
            try:
                int(content[i])
                if i not in col_type['foreign']:
                    col_type['integer'].append(i)
            except ValueError:
                try:
                    float(content[i])
                    col_type['decimal'].append(i)
                except ValueError:
                    col_type['date' if re.match(date_pattern, content[i], re.MULTILINE) else 'string'].append(i)

        return col_type
