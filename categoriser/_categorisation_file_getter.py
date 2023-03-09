from ._utils import Directory

__all__ = ["CategorisationFileGetter"]


class CategorisationFileGetter:
    SPREADSHEET_FOLDER_NAME = "cleaned_databases"
    CATEGORIZATION_FOLDER_NAME = "categorizations"

    def __init__(self, data_folder: Directory):
        self.__spreadsheet_folder = \
            data_folder.find_directory(
                CategorisationFileGetter.SPREADSHEET_FOLDER_NAME
            )
        data_folder.create_subdirectory(
            CategorisationFileGetter.CATEGORIZATION_FOLDER_NAME
        )
        self.__categorization_folder = \
            data_folder.find_directory(
                CategorisationFileGetter.CATEGORIZATION_FOLDER_NAME
            )

    @property
    def all_files(self):
        return set(map(lambda file: file.get_filename(),
                       self.__spreadsheet_folder.get_all_files()))

    @property
    def output_folder(self):
        return self.__categorization_folder
