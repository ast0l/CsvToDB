import abc


class Column(abc.ABC):

    def __repr__(self):
        return 'interface to make sql column'

    @abc.abstractmethod
    def _integer(self, column_value: list, column_name: str) -> str:
        """
        create column for int value\n

        **value:**\n
        dict of all value in the selected column\n

        **column_name**\n
        name given to the column\n

        :param column_value: dict
        :param column_name: str
        :return: str
        """
        pass

    @abc.abstractmethod
    def _decimal(self, column_value: list, column_name: str) -> str:
        """
        create column for float value\n

        **value:**\n
        dict of all value in the selected column\n

        **column_name**\n
        name given to the column\n

        :param column_value: dict
        :param column_name: str
        :return: str
        """
        pass

    @abc.abstractmethod
    def _string(self, column_value: list, column_name: str, char_set: str, collation: str) -> str:
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

    @abc.abstractmethod
    def _date(self, column_value: list, column_name: str) -> str:
        """
        create column for date value\n

        **value:**\n
        dict of all value in the selected column\n

        **column_name**\n
        name given to the column\n

        :param column_value: dict
        :param column_name: str
        :return: str
        """
        pass

    @abc.abstractmethod
    def _primary(self) -> str:
        """
        create the primary key
        :return: str
        """
        pass

    @abc.abstractmethod
    def _foreign(self, column_value: list, column_name: str) -> str:
        pass
