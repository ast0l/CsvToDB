import csv
import json
import re


class Csv:

    def __init__(self, filename: str, filepath: str, delimiter: str = ',', quoter: str = '"'):
        self.__filename: str = filename
        self.__filepath: str = filepath
        self.__delimiter: str = delimiter
        self.__quoter: str = quoter

    def __repr__(self):
        return 'class to edit or read csv data'

    def total_column(self) -> int:
        """
        return total column in the csv
        :return: int
        """
        return len(tuple(csv.reader(open(f'{self.__filepath}/{self.__filename}', 'r'),
                                    delimiter=self.__delimiter,
                                    quotechar=self.__quoter))[0])

    def row_list(self, limit: int = 0) -> tuple:
        """
        get list of row:\n
        limit = 1 return the first row\n
        limit = 2 return the first two rows\n
        etc...\n
        and start at the first data row

        :return:
        """
        if limit > 0:
            return tuple(csv.reader(open(f'{self.__filepath}/{self.__filename}.csv', 'r'),
                                    delimiter=self.__delimiter,
                                    quotechar=self.__quoter))[1:limit + 1]
        else:
            return tuple(csv.reader(open(f'{self.__filepath}/{self.__filename}.csv', 'r'),
                                    delimiter=self.__delimiter,
                                    quotechar=self.__quoter))[1:]

    def column_content(self, column: int):
        """
        return all row for one column\n

        **column -> int:**\n
        this param must contain column index from your file
        column index start at 1 not 0\n

        :param column: str
        :return: dict
        """
        column -= 1
        data: list = []
        with open(f'{self.__filepath}/{self.__filename}.csv', 'r') as file:
            read = csv.reader(file, delimiter=self.__delimiter, quotechar=self.__quoter)
            for row in read:
                data.append(row[column])
        file.close()
        return data

    def column_name(self) -> tuple:
        """
        return name of column
        :return:
        """
        column: tuple = tuple(csv.reader(open(f'{self.__filepath}/{self.__filename}.csv', 'r'),
                                         delimiter=self.__delimiter, quotechar=self.__quoter))[0]
        return tuple(column)

    def total_row(self) -> int:
        """
        return total of row

        :return:
        """
        return len(tuple(csv.reader(open(f'{self.__filepath}/{self.__filename}.csv', 'r'),
                                    delimiter=self.__delimiter, quotechar=self.__quoter)))

    def update_column_name(self, old, new):
        """
        set the name of one or more column\n

        **old:**\n
        column name to change in the csv_file, if you want change
        only one name it must be str and if you want to change name of multiple column
        it must be tuple\n

        **new:**\n
        new is the new column name, if you have precise str in actual this param must be str else
        this param must be tuple\n

        :return:
        """
        # check if param are correct
        if (type(old) is not str and type(old) is not tuple) or (type(new) is not str and type(new) is not tuple):
            raise TypeError('actual and new must be str or tuple')

        # check if param match
        if type(old) is str and type(new) is not str:
            raise TypeError('new must be str')
        elif type(old) is tuple:
            if type(new) is not tuple:
                raise TypeError('new must be tuple')
            # check if same number elem in each tuple
            if len(old) == len(new):
                for value in old:
                    if type(value) is not str:
                        raise TypeError('tuple for actual must contain only str')
                for value in new:
                    if type(value) is not str:
                        raise TypeError('tuple for new must contain only str')
            else:
                raise ValueError('You must have the same element in both tuples')

        try:
            # get value
            csv_data = list(csv.reader(open(f'{self.__filepath}/{self.__filename}', 'r'),
                                       delimiter=self.__delimiter, quotechar=self.__quoter))

            # change value
            if isinstance(old, str):
                for name in csv_data[0]:
                    if name == old:
                        i: int = csv_data[0].index(name)
                        csv_data[0][i] = new
                        del i
            else:
                for name in csv_data[0]:
                    if name in old:
                        csv_data[0][csv_data[0].index(name)] = new[old.index(name)]

            # write value
            csv.writer(open(f'{self.__filepath}/{self.__filename}', 'w', newline='')).writerows(csv_data)
            del csv_data, name
        except csv.Error as e:
            print(f'Error with the csv_file: {e}')

    def new_row(self, data: list, start: bool = False):
        """
        insert new row in the csv_file\n

        **data:**\n
        data represent the data you want to insert in the row

        **start:**\n
        default is False, set it to True if you want insert row at the start of file
        (after the first row which define column)\n

        :return:
        """
        try:
            csv_data: list = list(csv.reader(open(f'{self.__filepath}/{self.__filename}', 'r'), delimiter=self.__delimiter, quotechar=self.__quoter))
            if len(data) == len(csv_data[0]):
                csv_data.append(data) if not start else csv_data.insert(1, data)
            else:
                raise ValueError(f'your data list must have {len(csv_data[0])} column')
            csv.writer(open(f'{self.__filepath}/{self.__filename}', 'w', newline='')).writerows(csv_data)
        except csv.Error as e:
            print(e)

    def update_row(self, old, new, row: int = 0):
        """
        change value in row for one or more data

        **old:**\n
        the actual value in the row\n

        **new:**\n
        the new value to set in the row\n

        **row:**\n
        the line where to do the changes if row = 0 the modification are done on all row\n

        :return:
        """
        # check type
        if not isinstance(old, str) and not isinstance(old, tuple):
            raise TypeError('old must be str or tuple')
        if not isinstance(new, str) and not isinstance(new, tuple):
            raise TypeError('new must be str or tuple')
        if type(old) != type(new):
            raise TypeError('old and new must have same type')
        if isinstance(old, tuple):
            if len(old) != len(new):
                raise ValueError('old and new must have same length')
            for elem in old:
                if not isinstance(elem, str) and not isinstance(elem, int):
                    raise ValueError('old must contain str or int value only')
            for elem in new:
                if not isinstance(elem, str) and not isinstance(elem, int):
                    raise ValueError('new must contain str or int value only')

        try:
            csv_data = list(csv.reader(open(f'{self.__filepath}/{self.__filename}', 'r'), delimiter=self.__delimiter, quotechar=self.__quoter))

            if row == 0:
                if isinstance(old, str):
                    for elem in csv_data:
                        if old in elem:
                            elem[elem.index(old)] = new
                else:
                    for elem in csv_data:
                        for value in old:
                            if value in elem:
                                elem[elem.index(value)] = new[old.index(value)]
            else:
                if isinstance(old, str) and old in csv_data[row]:
                    csv_data[row][csv_data[row].index(old)] = new
                else:
                    for value in old:
                        if value in csv_data[row]:
                            csv_data[row][csv_data[row].index(value)] = new[old.index(value)]

            csv.writer(open(f'{self.__filepath}/{self.__filename}', 'w', newline='')).writerows(csv_data)
        except csv.Error as e:
            print(e)

    def to_json(self, path: str, filename: str, get_col_name: bool = False, key_on_value: bool = False) -> bool:
        """
        create json file with data from csv_file, return True if the file already exist return False\n

        **_filename:**\n
        _filename represent the name to use when file is create\n

        **path:**\n
        path is where to save the file\n

        **get_col_name:**\n
        add column name in the json\n

        **key_on_value:**\n
        This will refer each value in each row with for key the corresponding column\n

        :param path: str
        :param filename: str
        :param get_col_name: bool
        :param key_on_value: bool
        :return: bool
        """
        try:
            with open(f'{self.__filepath}/{self.__filename}', 'r') as file:
                csv_data: list = list(csv.reader(file, delimiter=self.__delimiter, quotechar=self.__quoter))
                total: int = 1
                # check if need col name
                if get_col_name:
                    data: dict = {'column': csv_data[0]}
                else:
                    data: dict = {}

                # check if need key on value
                if key_on_value:
                    column: list = csv_data[0]
                    del csv_data[0]
                    for elem in csv_data:
                        row: dict = {}
                        for value in elem:
                            row[column[elem.index(value)]] = value
                        data[total] = row
                        total += 1
                else:
                    del csv_data[0]
                    for elem in csv_data:
                        data[total] = elem
                        total += 1
            file.close()

            with open(f'{path}/{filename}.json', 'x') as file:
                json.dump(data, file)
            file.close()

            return True
        except csv.Error as e:
            print(f'error with your csv_file {e}')
        except FileExistsError:
            return False

    def format_column_name(self):
        """
        format column name
        :return:
        """
        data: list = list(csv.reader(open(f'{self.__filepath}/{self.__filename}.csv', 'r'),
                                     delimiter=self.__delimiter, quotechar=self.__quoter))
        data[0] = [re.sub(r' ', '_', data[0][i], 0, re.MULTILINE) for i in range(0, len(data[0]))]
        csv.writer(open(f'{self.__filepath}/{self.__filename}.csv', 'w', newline='')).writerows(data)

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

    def set_filename(self, filename: str):
        """
        set _filename to use
        :param filename:
        """
        self.__filename = filename

    def get_filename(self) -> str:
        """
        return _filename used
        :return: str
        """
        return self.__filename

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
    p_filename = property(fget=get_filename, fset=set_filename)
    p_file_delimiter = property(fget=get_delimiter, fset=set_delimiter)
    p_file_quoter = property(fget=get_quoter, fset=set_quoter)
