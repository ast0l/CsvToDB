import abc
from csvtodb.Csv import Csv


class Table:
    def __repr__(self):
        return 'method used to build table'

    @abc.abstractmethod
    def build_table(self, csv: Csv, engine: str, temporary: bool) -> str:
        """
        create new sql table

        :param csv: Csv
        :param engine: str
        :param temporary: bool
        :return: str
        """
        pass
