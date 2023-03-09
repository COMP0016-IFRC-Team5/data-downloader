from ._utils import Directory
from ._classifier import Classifier
from ._categorisation_file_getter import CategorisationFileGetter

__all__ = ["CategorisationController"]


class CategorisationController:
    @staticmethod
    def start_categorize(data_folder: Directory):
        file_getter = CategorisationFileGetter(data_folder)
        output_folder = file_getter.output_folder
        event_types = set(
            map(
                lambda filename: filename.lower(),
                file_getter.all_files
            )
        )
        classifier = Classifier(event_types)
        categorisations = classifier.categorisations
        CategorisationController.__write_categorisations(
            output_folder, categorisations
        )

    @staticmethod
    def __write_categorisations(output_folder, categorisations):
        for event, extracted_types in categorisations:
            output_filepath = \
                f"{output_folder.get_path()}/{event}.txt"
            CategorisationController.__write_to_file(
                output_filepath, extracted_types
            )

    @staticmethod
    def __write_to_file(filename, content):
        content = sorted(list(content))
        with open(filename, mode='w', encoding='UTF-8') as f:
            f.writelines(map(lambda line: f"{line}\n", content))
