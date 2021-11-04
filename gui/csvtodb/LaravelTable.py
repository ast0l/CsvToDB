import re
from csvtodb.Csv import Csv
from generic.Table import Table
from laravel.LaravelColumn import LaravelColumn


class LaravelTable(Table, LaravelColumn):
    def __repr__(self):
        return 'build table for laravel'

    @classmethod
    def _build_table(cls, csv: Csv,  engine: str, temporary: bool) -> str:
        """
        build new migration table for Laravel
        for the up function
        :param csv:
        :param engine:
        :param temporary:
        :return:
        """
        columns: dict = cls._define_col_type(csv)

        new_table: str = '\n\t\tSchema::create("%s", function(Blueprint $table){\n' % csv.p_filename
        new_table += f'\t\t\t$table->engine = "{engine}";\n'
        if temporary:
            new_table += '\t\t\t$table->temporary();\n'
        new_table += cls._primary()

        for column in columns:
            if columns[column]:
                if column == 'integer':
                    for i in columns[column]:
                        content: list = csv.column_content(column=i + 1)
                        name: str = content.pop(0)
                        new_table += cls._integer(column_value=content, column_name=name)
                elif column == 'decimal':
                    for i in columns[column]:
                        content: list = csv.column_content(column=i + 1)
                        name: str = content.pop(0)
                        new_table += cls._decimal(column_value=content, column_name=name)
                elif column == 'string':
                    for i in columns[column]:
                        content: list = csv.column_content(column=i + 1)
                        name: str = content.pop(0)
                        new_table += cls._string(column_value=content, column_name=name)
                elif column == 'date':
                    for i in columns[column]:
                        content: list = csv.column_content(column=i + 1)
                        name: str = content.pop(0)
                        new_table += cls._date(column_value=content, column_name=name)
                elif column == 'foreign':
                    for i in columns[column]:
                        content: list = csv.column_content(column=i+1)
                        name: str = content.pop(0)
                        new_table += f'{cls._foreign(column_value=content, column_name=name)},\n'

        new_table += '\t\t});\n'
        return new_table

    @classmethod
    def _down(cls, csv: Csv):
        """
        used for the down function to remove table

        :param csv:
        :return:
        """
        return f'\t\tSchema::dropIfExists("{csv.p_filename}");\n'

    @classmethod
    def _define_col_type(cls, csv: Csv):
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
