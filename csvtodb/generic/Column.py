import abc


class Column(abc.ABC):

    def __init__(self, name: str, value: list):
        self._name = name
        self._value = value

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
        create column for string value\n

        **value:**\n
        dict of all value in the selected column\n

        **column_name**\n
        name given to the column\n

        **char_set**\n
        Character set to use\n

        **collation**\n
        collation to use\n

        :param column_value: dict
        :param column_name: str
        :param char_set: str
        :param collation: str
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