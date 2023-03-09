from ._country import Country

__all__ = ['Disaster', 'Disasters']


class Disaster:
    def __init__(self, name_en: str, query_key: str):
        """Data class for storing a type of disaster

        Parameters
        ----------
        name_en : str
            English name of the disaster, but it may also be written in other
            languages such as French and Spanish
        query_key : str
            The name to use when querying the database.
        """
        self.__name_en = name_en.replace('/', '+')
        self.__query_key = query_key

    @property
    def name(self):
        """str: English name of the disaster"""
        return self.__name_en

    def set_new_name(self, new_name: str):
        """Change the English name of the disaster

        This method mainly renames disaster names when more than one disaster
        name has the same characters regardless of case.

        Parameters
        ----------
        new_name : str
            New name for the disaster
        """
        self.__name_en = new_name

    @property
    def query_key(self):
        """str: The name to use when querying the database."""
        return self.__query_key


class Disasters:
    def __init__(self, country: Country):
        """Data class for storing all disaster types of a country

        Parameters
        ----------
        country : Country
            The target country

        See Also
        --------
        .Country.Country : Data class for storing a country
        """
        self.__country = country
        self.__disaster_list: list[Disaster] = []

    def add_disaster(self, disaster: Disaster):
        """Add a disaster type

        Parameters
        ----------
        disaster : Disaster
            Disaster to be added
        """
        self.__disaster_list.append(disaster)

    def rename_duplicate_disasters(self):
        """Rename disasters with the same name regardless of case

        Notes
        -----
        Disasters with name as ACCIDENT, accident and flood will be renamed as
        ACCIDENT_1, accident_2 and flood
        """
        disaster_names_list = [d.name.upper() for d in self.__disaster_list]
        for i, d in enumerate(self.__disaster_list):
            total_count = disaster_names_list.count(d.name.upper())
            count = disaster_names_list[:i].count(d.name.upper())
            d.set_new_name(
                f"{d.name}_{str(count + 1)}" if total_count > 1 else d.name)

    def __iter__(self):
        return iter(self.__disaster_list)
