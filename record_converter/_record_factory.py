import bs4

from ._record import Record

__all__ = ["RecordFactory"]


class RecordFactory:
    _entry_translation = {
        'muertos': 'deaths',
        'heridos': 'injured',
        'desaparece': 'missing',
        'vivdest': 'houses_destroyed',
        'vivafec': 'houses_damaged',
        'damnificados': 'directly_affected',
        'afectados': 'indirectly_affected',
        'reubicados': 'relocated',
        'evacuados': 'evacuated',
        'valorus': 'losses_in_dollar',
        'valorloc': 'losses_local_currency',
        'nescuelas': 'education_centers',
        'nhospitales': 'hospitals',
        'nhectareas': 'damages_in_crops_ha',
        'cabezas': 'lost_cattle',
        'kmvias': 'damages_in_roads_mts',
        'serial': 'serial',
        'level0': 'level0',
        'level1': 'level1',
        'level2': 'level2',
        'name0': 'name0',
        'name1': 'name1',
        'name2': 'name2',
        "evento": "event",
        "lugar": "location",
        "fechano": "year",
        "fechames": "month",
        "fechadia": "day",
        'approved': 'approved',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'uu_id': 'uuid'
    }

    @staticmethod
    def __get_value(text: str):
        if not text:
            return text

        def is_int():
            try:
                int(text)
                return True
            except ValueError:
                return False

        def is_float():
            try:
                float(text)
                return True
            except ValueError:
                return False

        if is_int():
            return int(text)
        elif is_float():
            return float(text)
        else:
            return text

    @staticmethod
    def from_tag(tag: bs4.Tag) -> Record:
        record = Record()
        translation = RecordFactory._entry_translation
        for xml_tag_name, attr_name in translation.items():
            attr_val = tag.find(xml_tag_name)
            if attr_val is None and xml_tag_name == "kmvias":
                attr_val = tag.find("Kmvias")
            value = RecordFactory.__get_value(attr_val.text)
            setattr(record, attr_name, value)
        return record

    @staticmethod
    def from_list(tags: list[bs4.Tag]) -> list[Record]:
        return list(
            map(
                lambda tag: RecordFactory.from_tag(tag),
                tags
            )
        )
