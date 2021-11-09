import re
from abc import ABC

from generic.Table import Table
from mysql.MysqlColumn import MysqlColumn
from csvtodb.Csv import Csv


class MysqlTable(Table, MysqlColumn, ABC):

    __ENGINE: tuple = ('innodb', 'myisam', 'memory', 'csv')

    def __repr__(self):
        return 'class to build sql table for mysql'

    def _build_table(self, csv: Csv, engine: str, temporary: bool) -> str:
        pass
