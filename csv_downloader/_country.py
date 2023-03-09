__all__ = ['Country']


class Country:
    def __init__(self, url: str, name: str):
        """Data class for storing a country's information

        Parameters
        ----------
        url : str
            The URL for the country's web page in DesInventar
        name : str
            Name of the country
        """
        self.__url = url
        self.__name = name
        self.__country_code = url.split('countrycode=')[1].split('&')[0]

    def get_url(self):
        """str: Returns the url of the country's web page"""
        return self.__url

    def get_name(self):
        """str: Returns the name of the country"""
        return self.__name

    def get_country_code(self):
        """str: Returns the country code of the country"""
        return self.__country_code
