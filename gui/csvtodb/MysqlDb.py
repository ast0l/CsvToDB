from generic.Database import Database
from mysql.MysqlTable import MysqlTable
from csvtodb.Csv import Csv


class MysqlDb(Database, MysqlTable):

    def __repr__(self):
        return 'class to build new db'

    @classmethod
    def _build_db(cls, db_name: str, files: dict, engine: str):
        """
        build new db with table

        **files:**\n
        files need to be\n
        {\n
        'path_to_files_1': ((csv_filename_1, delimiter, quotechar), (csv_filename_1, delimiter, quotechar), etc...)\n
        'path_to_files_2': ((csv_filename_1, delimiter, quotechar), (csv_filename_1, delimiter, quotechar), etc...)\n
        }\n

        :return:
        """
        csv = Csv(filename='', filepath='', delimiter='', quoter='')
        file = f'CREATE DATABASE IF NOT EXISTS {db_name};\n\nUSE {db_name};\n\n'
        for i in files:
            for j in range(0, len(files[i])):
                csv.p_filepath = i
                csv.p_filename = files[i][j][0]
                csv.p_file_delimiter = files[i][j][1]
                csv.p_file_quoter = files[i][j][2]
                file += cls._build_table(csv=csv, engine=engine, temporary=False)
        return file

    @classmethod
    def _build_tables(cls, files: dict, engine: str):
        """
        build multiple table

        **files:**\n
        files need to be\n
        {\n
        'path_to_files_1': ((csv_filename_1, delimiter, quotechar), (csv_filename_1, delimiter, quotechar), etc...)\n
        'path_to_files_2': ((csv_filename_1, delimiter, quotechar), (csv_filename_1, delimiter, quotechar), etc...)\n
        }\n

        :return:
        """
        csv = Csv(filename='', filepath='', delimiter='', quoter='')
        file = ''
        for i in files:
            for j in range(0, len(files[i])):
                csv.p_filepath = i
                csv.p_filename = files[i][j][0]
                csv.p_file_delimiter = files[i][j][1]
                csv.p_file_quoter = files[i][j][2]
                file += cls._build_table(csv=csv, engine=engine, temporary=False)
        return file
