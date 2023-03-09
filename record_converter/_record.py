from math import isclose


__all__ = ["Record"]


class Record:
    def __init__(self):
        self.deaths: int | None = None
        self.injured: int | None = None
        self.missing: int | None = None
        self.houses_destroyed: int | None = None
        self.houses_damaged: int | None = None
        self.directly_affected: int | None = None
        self.indirectly_affected: int | None = None
        self.relocated: int | None = None
        self.evacuated: int | None = None
        self.losses_in_dollar: float | None = None
        self.losses_local_currency: float | None = None
        self.education_centers: int | None = None
        self.hospitals: int | None = None
        self.damages_in_crops_ha: float | None = None
        self.lost_cattle: int | None = None
        self.damages_in_roads_mts: float | None = None
        self.serial: int | None = None
        self.level0: int | None = None
        self.level1: int | None = None
        self.level2: int | None = None
        self.year: int | None = None
        self.month: int | None = None
        self.day: int | None = None
        self.approved: int | None = None
        self.latitude: float | None = None
        self.longitude: float | None = None
        self.uuid: str | None = None
        self.name0: str | None = None
        self.name1: str | None = None
        self.name2: str | None = None
        self.event: str | None = None
        self.location: str | None = None

    def __guard_attributes(self):
        for k, v in self.__dict__.items():
            if v is None:
                raise ValueError(f"None value is detected for self.{k}")

    def __repr__(self):
        return "".join(f"\t{k}: {v}\n" for k, v in self.__dict__.items()) + \
            f"\tdate: {self.date}\n"

    def as_dict(self) -> dict:
        tmp_dict = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['year', 'month', 'day']
        }
        tmp_dict['date'] = self.date
        return tmp_dict

    @property
    def date(self):
        return f"{self.day}/{self.month}/{self.year}"

    @property
    def location_code(self):
        return self.level2

    @property
    def __int_data(self):
        return self.deaths, self.injured, self.missing, self.houses_destroyed, \
            self.houses_damaged, self.directly_affected, \
            self.indirectly_affected, self.relocated, self.evacuated, \
            self.education_centers, self.hospitals, self.lost_cattle

    @property
    def __float_data(self):
        return self.losses_in_dollar, self.losses_local_currency, \
            self.damages_in_crops_ha, self.damages_in_roads_mts

    def is_same_event(self, other):
        self.__guard_attributes()
        if other.__class__ != self.__class__:
            return False
        return self.date == other.date \
            and self.location_code == other.location_code

    def __is_duplicate(self, other):
        return self.__int_data == other.__int_data \
            and all(
                isclose(val_1, val_2)
                for val_1, val_2
                in zip(self.__float_data, other.__float_data)
            )

    def has_duplication(self, other):
        return self.__is_duplicate(other) \
            if self.is_same_event(other) else False
