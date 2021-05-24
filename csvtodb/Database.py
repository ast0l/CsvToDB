import abc


class Database:

    def __repr__(self):
        return 'interface to create new database'

    @abc.abstractmethod
    def _build_db(self, db_name: str, files: dict, engine: str) -> str:
        """
        create new database
        :return:
        """
        pass
