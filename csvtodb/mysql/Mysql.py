from abc import ABC

from csvtodb.Csv.Csv import Csv
from csvtodb.mysql.MysqlDb import MysqlDb
from csvtodb.mysql.MysqlTable import Table


class Mysql(MysqlDb, ABC):

    def __init__(self, csv: list[Csv], engine: str = 'INNODB', credential: tuple = None):
        self.__csv: list[Csv] = csv
        self.__engine: str = engine
        self.credential: tuple = credential

    def __repr__(self):
        return 'create database or table from csv for Mysql'

    def build_db(self, db_name: str) -> bool:
        file_content = f'CREATE DATABASE IF NOT EXISTS {db_name};\n\nUSE {db_name};\n\n'
        try:
            file = open(f'{db_name}.sql', 'x')
            file.write(file_content)
        except FileExistsError:
            with open(f'{db_name}.sql', 'w') as file:
                file.write(file_content)
        file.close()
        return True

    def build_table(self) -> bool:
        """
        create new table for the specified file contained in the csv list
        :return: bool
        """
        pass

    def build_tables(self):
        """
        build multiple table from multiple csv file\n

        **filepath:**\n
        where to save the file\n

        **_filename:**\n
        name of the saved file\n

        **files**\n
        content all files to build in table, it must be construct like this:\n
        files need to be\n
        {\n
        'path_to_files_1': ((csv_filename_1, delimiter, quotechar), (csv_filename_1, delimiter, quotechar), etc...)\n
        'path_to_files_2': ((csv_filename_1, delimiter, quotechar), (csv_filename_1, delimiter, quotechar), etc...)\n
        }\n

        :return:
        """
        pass

    def build_seeder(self):
        """
        build seeder from file

        **filepath:**\n
        where to save the file\n

        **filename:**\n
        name of the saved file\n

        :param csv:
        :param filepath:
        :param filename:
        :return:
        """
        pass
