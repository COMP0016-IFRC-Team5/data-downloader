import dill
import os

__all__ = ['Dumper']


class Dumper:
    def __init__(self):
        """Util class for saving a cache of an object

        Notes
        -----
        The caches will be stored in the ``current_folder/caches`` folder.
        ``current_folder`` is the directory of ``_object_dumper.py``
        """
        current_folder = os.path.dirname(os.path.realpath(__file__))
        self.__cache_folder = f"{current_folder}/caches"
        if not os.path.exists(self.__cache_folder):
            os.makedirs(self.__cache_folder)

    def cache(self, obj, name: str):
        """Save a cache of an object

        Parameters
        ----------
        obj
            Object to be cached
        name : str
            Name of the cache

        Raises
        ------
        FileNotFoundError
            If the name is a path and not created.
        """
        with open(self.__get_cache_path(name), 'wb') as f:
            dill.dump(obj, f)

    def __get_cache_path(self, name: str):
        return f"{self.__cache_folder}/{name}"

    def has_cache(self, name: str):
        """Check if cache folder contains a cache with name ``name``

        Parameters
        ----------
        name : str
            Name of the cache

        Returns
        -------
        bool
            Existence of the cache requested
        """
        return os.path.exists(self.__get_cache_path(name))

    def load(self, name: str):
        """Load the cache with name ``name``

        Parameters
        ----------
        name : str
            Name of the cache

        Returns
        -------
        object
            Loaded object

        Raises
        ------
        FileNotFoundError
            If cache folder does not contain the requested cache
        """
        if not self.has_cache(name):
            raise FileNotFoundError(
                f"Object cache with name '{name}' does not exist.")
        with open(self.__get_cache_path(name), 'rb') as f:
            return dill.load(f)

    def get_cache_folder(self):
        """Returns the path of the cache folder

        Returns
        -------
        str
            The path of the cache folder
        """
        return self.__cache_folder
