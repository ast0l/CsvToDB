import abc


class Column(abc.ABC):

    def __repr__(self):
        return 'Method for building column'

    def _integer(self) -> str:
        """
        create integer number column
        :return: str
        """
        pass

    def _decimal(self) -> str:
        """
        create column for decimal number
        :return: str
        """
        pass

    def _string(self) -> str:
        """
        create column for string value
        :return: str
        """
        pass

    def _date(self) -> str:
        """
        create column for date value
        :return: str
        """
        pass

    def _primary(self) -> str:
        """
        create the primary key
        :return: str
        """
        pass

    def _foreign(self) -> str:
        """
        create foreign key
        :return: str
        """
        pass

    def __get_type(self):
        """
        get the type for column
        """
        pass

    def build(self) -> str:
        """
        build the column
        :return:
        """