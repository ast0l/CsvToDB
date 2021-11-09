import abc


class Database:
    def __repr__(self):
        return 'interface to create new database'

    @abc.abstractmethod
    def build(self, db_name: str) -> str:
        """
        create new database
        :return str:
        """
        pass
