import abc
from csvtodb.Csv import Csv


class Table:
    def __repr__(self):
        return 'interface to make sql table'

    @abc.abstractmethod
    def _build_table(self, csv: Csv, engine: str, temporary: bool) -> str:
        """
        create new sql table

        :param csv: Csv
        :param engine: str
        :param temporary: bool
        :return: str
        """
        pass

    @abc.abstractmethod
    def _define_col_type(self, csv: Csv):
        pass
