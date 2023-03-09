import os
import gc
from typing import Optional, List

import bs4
import pandas as pd

from ._record_factory import RecordFactory

__all__ = ["RecordsConverter"]


class RecordsConverter:
    _ORIGINAL_DATABASE_FOLDER_NAME = "XMLdatabases"
    _RECORDS_FOLDER_NAME = "records"

    def __init__(self):
        self.__data_folder: Optional[str] = None
        self.__original_database_folder: Optional[str] = None
        self.__files: Optional[List[str]] = None

    def __get_data_folder(self):
        if self.__data_folder is None:
            raise ValueError("Directory has not been set.")
        return self.__data_folder

    def set_data_folder(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path does not exist:\n {path}")
        self.__data_folder = path

    def start_conversion(self):
        self.__get_file_paths()
        self.__convert_all_databases()

    def __get_file_paths(self):
        self.__original_database_folder = \
            f"{self.__get_data_folder()}/" \
            f"{RecordsConverter._ORIGINAL_DATABASE_FOLDER_NAME}"
        self.__files = os.listdir(self.__original_database_folder)
        self.__files = list(
            map(
                lambda file:
                os.path.abspath(f"{self.__original_database_folder}/{file}"),
                self.__files
            )
        )

    def __convert_all_databases(self):
        for file in self.__files:
            self.__convert_database(file)

    @staticmethod
    def __get_soup(file: str):
        with open(file, "r") as fp:
            soup = bs4.BeautifulSoup(fp, "xml")
        return soup

    def __get_records_folder(self):
        folder = f"{self.__get_data_folder()}/" \
                 f"{RecordsConverter._RECORDS_FOLDER_NAME}"
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def __from_soup(self, file):
        soup = self.__get_soup(file)
        record_tags: bs4.Tag = soup.DESINVENTAR.fichas
        return record_tags.find_all('TR')

    def __from_file(self, file):
        raw_records = self.__from_soup(file)
        gc.collect()
        return list(
            map(
                lambda rec: rec.as_dict(),
                RecordFactory.from_list(raw_records)
            )
        )

    def __convert_database(self, file: str):
        country_name = file.split('/')[-1][:-4]
        csv_file = f"{self.__get_records_folder()}/{country_name}.csv"
        if os.path.exists(csv_file):
            print(f"{csv_file} exists, skip")
            return
        print(f"converting {csv_file} ...")
        records = self.__from_file(file)
        gc.collect()
        # noinspection PyTypeChecker
        df = pd.DataFrame.from_dict(records)
        del records
        gc.collect()
        # same_event = df[df.duplicated(['date', 'level2'], keep=False)]
        with open(csv_file, 'w') as f:
            df.to_csv(f, index=False)
