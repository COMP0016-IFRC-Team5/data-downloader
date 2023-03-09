from ._categorisations import ALL_SUBTYPES

__all__ = ["Classifier"]


class Classifier:
    def __init__(self, event_types: set):
        self.__categorisations = []
        for event, subtypes in ALL_SUBTYPES.items():
            event_types, extracted_types = Classifier.__extract_types(
                subtypes, event_types
            )
            self.__categorisations.append((event, extracted_types))
        if '.ds_store' in event_types:
            event_types.remove('.ds_store')
        self.__categorisations.append(('Other', event_types))

    @property
    def categorisations(self):
        return self.__categorisations

    @staticmethod
    def __extract_types(subtypes, event_types):
        subtype_files = \
            Classifier.__get_all_subtype_filenames(subtypes, event_types)
        events = {event_type for event_type in event_types if
                  event_type not in subtype_files}
        return events, subtype_files

    @staticmethod
    def __get_all_subtype_filenames(types, all_categories):
        return [
            event
            for event in all_categories
            if Classifier.__types_in_event(types, event)
        ]

    @staticmethod
    def __types_in_event(types, event):
        return any(event_type in event.replace(' ', '') for event_type in
                   Classifier.__remove_spaces(types))

    @staticmethod
    def __remove_spaces(str_set: set[str]):
        return set(
            map(
                lambda elem: elem.replace(' ', ''),
                str_set
            )
        )
