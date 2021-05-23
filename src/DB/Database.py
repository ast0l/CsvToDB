import abc


class Database:

    def __repr__(self):
        return 'interface to create new database'

    @abc.abstractmethod
    def _build_db(self, name: str) -> str:
        """
        create new database
        :return:
        """
        pass

    @abc.abstractmethod
    def _insert_db(self):
        """
        create new db directly in server
        :return:
        """
        pass
