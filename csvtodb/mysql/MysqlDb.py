from csvtodb.generic.Database import Database
from abc import ABC, abstractmethod


class MysqlDb(Database, ABC):
    def __repr__(self):
        return 'class to build new db'

    @abstractmethod
    def build_db(self, db_name: str) -> bool:
        """
        used to build database, it will create new db AND add all csv passed as table
        :param db_name:
        :return:
        """
        pass

