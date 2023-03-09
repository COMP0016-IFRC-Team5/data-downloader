from ._categorisation_controller import CategorisationController
from ._utils import Directory

__all__ = ["start"]


def start(path: str):
    data_folder = Directory(path)
    CategorisationController.start_categorize(data_folder)
