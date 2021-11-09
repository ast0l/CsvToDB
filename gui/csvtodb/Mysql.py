import re

from csvtodb.Csv import Csv
from mysql.MysqlDb import MysqlDb


class Mysql(MysqlDb):

    def __repr__(self):
        return 'build db or table or both with using mysql'

    @classmethod
    def new_db(cls, save_in: str, db_name: str, files: dict, engine: str = 'INNODB'):
        """
        build new db with table\n

        **files:**\n
        files need to be\n
        {\n
        'path_to_files_1': ((csv_filename_1, delimiter, quotechar), (csv_filename_1, delimiter, quotechar), etc...)\n
        'path_to_files_2': ((csv_filename_1, delimiter, quotechar), (csv_filename_1, delimiter, quotechar), etc...)\n
        }\n

        :return:
        """
        try:
            with open(f'{save_in}/{db_name}.sql', 'x') as file:
                file.write(cls._build(db_name=db_name, files=files, engine=engine))
            file.close()
            return True
        except FileExistsError:
            return False

    @classmethod
    def new_table(cls, csv: Csv, filepath: str, filename: str, engine: str = 'INNODB',
                  temporary: bool = False) -> bool:
        """
        create new table in file\n

        **filepath:**\n
        where to save the file\n

        **_filename:**\n
        name of the saved file\n

        **return type:**\n
        if all is ok (file created and content added) return true
        else if there is any error return false

        :return: bool
        """
        try:
            with open(f'{filepath}/{filename}.sql', 'x') as file:
                file.write(cls._build_table(csv=csv, engine=engine, temporary=temporary))
            file.close()
            return True
        except FileExistsError:
            with open(f'{filepath}/{filename}.sql', 'a') as file:
                file.write(cls._build_table(csv=csv, engine=engine, temporary=temporary))
            file.close()
            return True

    @classmethod
    def new_tables(cls, filepath: str, filename: str, files: dict, engine: str = 'INNODB'):
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
        try:
            with open(f'{filepath}/{filename}.sql', 'x') as file:
                file.write(cls._build_tables(files=files, engine=engine))
            file.close()
        except FileExistsError:
            with open(f'{filepath}/{filename}.sql', 'a') as file:
                file.write(cls._build_tables(files=files, engine=engine))
            file.close()

    @classmethod
    def new_seeder(cls, csv: Csv, filepath: str, filename: str):
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
        column_name: tuple = csv.column_name()
        seeder = re.sub(r"'", '', f'INSERT INTO {csv.p_filename} {column_name} VALUES\n', 0, re.MULTILINE)
        rows = csv.row_list()
        for i, row in enumerate(rows):
            seeder += f'\t{tuple(row)},\n' if i != len(rows)-1 else f'\t{tuple(row)};'
        try:
            with open(f'{filepath}/{filename}.sql', 'x') as file:
                file.write(seeder)
            file.close()
        except FileExistsError:
            with open(f'{filepath}/{filename}.sql', 'a') as file:
                file.write(seeder)
            file.close()
