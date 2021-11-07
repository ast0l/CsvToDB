import csv
import json
import re


class Csv:
    def __init__(self, file_absolute_path: str, delimiter: str = ',', quotechar: str = '"'):
        """
        file **must** be absolute path
        :param file_absolute_path:
        :param delimiter:
        :param quotechar:
        """
        self.__delimiter: str = delimiter
        self.__quotechar: str = quotechar
        self.__content: dict = {
            "total_column": None,
            "total_rows": None,
            "column_name": None,
            "rows": [],
        }

        # check path validity
        disk = re.match(r'^[aA-zZ]:\\$', file_absolute_path[:3], re.MULTILINE)  # check if path begin with disk
        file_ext = re.match(r'\.csv$', file_absolute_path[-4:], re.MULTILINE)  # check if file ext is csv

        if disk and file_ext:
            self.__file = file_absolute_path
        else:
            raise ValueError('Incorrect file path')

        # get the content of the file
        try:
            total_rows: int = 0

            # add all rows in the file
            with open(self.__file, 'r') as csv_file:
                for row in csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar):
                    self.__content['rows'].append(row)
                    total_rows += 1  # for total rows
                csv_file.close()
            total_rows -= 1  # remove 1 for column

            # get total of column
            if self.__content['rows']:
                # get column
                column = self.__content['rows'][0]
                del self.__content['rows'][0]  # remove column from the rows

                # set info about column
                self.__content['total_column'] = len(column)
                self.__content['column_name'] = column
                self.__format_column_name()

            self.__content['total_rows'] = total_rows
            print()
        except FileNotFoundError:
            raise FileNotFoundError('can\'t find your csv file')

    def __repr__(self):
        return 'class for editing or reading csv data'

    def total_column(self) -> int:
        """
        return total column in the csv
        :return: int
        """
        return self.__content['total_column']

    def get_rows(self, amount: int = None) -> list:
        """
        return amount of rows (all by default)
        :return tuple:
        """
        rows: list = self.__content['rows']

        if amount is not None:
            if amount <= self.__content['total_rows']:
                print(rows[:amount])
            else:
                raise ValueError(f'the amount must be equal of less than {len(rows)}')
        else:
            return rows

    def get_col_name(self) -> list:
        """
        return name of column
        :return:
        """
        return self.__content['column_name']

    def get_total_rows(self) -> int:
        """
        return total of row

        :return:
        """
        return self.__content['total_rows']

    def get_data(self) -> tuple:
        return self.__content['column_name'], self.__content['rows']

    def update_column_name(self, actual_name: str, new_name: str) -> bool:
        """
        update column name
        :return bool:
        """
        column: list = self.__content['column_name']

        # check actual name exist
        if actual_name in column:
            column[column.index(actual_name)] = new_name  # set the new name
            try:
                self.__format_column_name()
                self.__override_file()
                return True
            except csv.Error as e:
                raise
        else:
            raise ValueError(f'{actual_name} doesn\'t exist in the actual value')

    def add_new_row(self, new_row: list) -> bool:
        """
        insert new row in the csv
        :return:
        """
        try:
            # check if all col are fill
            if len(new_row) == self.__content['total_column']:
                self.__content['rows'].append(new_row)
                self.__override_file()
                return True
            else:
                raise ValueError(f'you must have {self.__content["total_column"]} element in your list')
        except csv.Error as e:
            raise csv.Error(f'something wrong happen with csv module {e}')

    def __format_column_name(self) -> bool:
        """
        format column name
        replace whitespace with underscore
        :return bool:
        """
        column = self.__content['column_name']

        for name in column:
            column[column.index(name)] = name.replace(' ', '_')

        self.__content['column_name'] = column

        print(self.__content['column_name'])
        return True

    def __override_file(self):
        """
        write in file value contain in self.__content['rows']
        :return:
        """
        try:
            self.__content['rows'].insert(0, self.__content['column_name'])  # add column name

            with open(self.__file, 'w', newline='') as f:
                csv.writer(f).writerows(self.__content['rows'])
                f.close()

            del self.__content['rows'][0]  # remove column name
        except csv.Error:
            raise csv.Error('something wrong happened when trying to override file')

    """
    ==================================================
    getter & setter
    ==================================================
    """
    def set_filepath(self, filepath: str):
        """
        set file to use
        :param filepath:
        """
        self.__filepath = filepath

    def get_filepath(self) -> str:
        """
        return path or only _filename used
        :return: str
        """
        return self.__filepath

    def set_delimiter(self, delimiter: str):
        """
        set delimiter in the file
        :param delimiter:
        """
        self.__delimiter = delimiter

    def get_delimiter(self) -> str:
        """
        return delimiter used
        :return: str
        """
        return self.__delimiter

    def set_quoter(self, quoter: str):
        """
        set delimiter in the file
        :param quoter:
        """
        self.__quoter = quoter

    def get_quoter(self) -> str:
        """
        return delimiter used
        :return: str
        """
        return self.__quoter

    p_filepath = property(fget=get_filepath, fset=set_filepath)
    p_file_delimiter = property(fget=get_delimiter, fset=set_delimiter)
    p_file_quoter = property(fget=get_quoter, fset=set_quoter)