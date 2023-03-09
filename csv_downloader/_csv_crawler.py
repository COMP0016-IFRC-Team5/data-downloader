import os
import time

from bs4 import BeautifulSoup
import requests
import logging

from ._country import Country
from ._object_dumper import Dumper
from ._disasters import Disaster, Disasters

__all__ = ['CSVCrawler']


class CSVCrawler:
    COUNTRY_CACHE_FILE = 'country_list.pkl'
    DISASTERS_CACHE_FILE = 'disasters.pkl'
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    DATABASES_DIRECTORY_NAME = f"raw_csv_files"

    def __init__(self, target_dir: str):
        self.__index_url = "https://www.desinventar.net/DesInventar/index.jsp"
        self.__base_url = "https://www.desinventar.net"
        self.__dumper = Dumper()
        self.__target_dir = target_dir

    @staticmethod
    def remove_newlines(contents):
        return list(filter(lambda tr: tr != '\n', contents))

    @staticmethod
    def retrieve_html_text(url) -> str:
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except requests.HTTPError:
            return ""

    def __retrieve_table_data(self):
        html_text = CSVCrawler.retrieve_html_text(self.__index_url)
        soup = BeautifulSoup(html_text, "lxml")
        raw_data = CSVCrawler.remove_newlines(soup.body.table.table.children)
        # remove table header: 'Country/Region'
        return raw_data[1:]

    def __retrieve_country_list(self):
        table_data = self.__retrieve_table_data()
        country_tags = [CSVCrawler.remove_newlines(c) for c in table_data]
        # <a href="/DesInventar/profiletab.jsp?
        # countrycode=alb&continue=y"> Albania</a>
        country_list = [Country(url=self.__base_url + lst[1].a['href'],
                                name=lst[1].a.string.strip())
                        for lst in country_tags]
        self.__dumper.cache(country_list, CSVCrawler.COUNTRY_CACHE_FILE)
        return country_list

    def __get_disasters(self, country, ignore_cache: int):
        cache_name = f"disasters/{country.get_name()}_" \
                     f"{country.get_country_code()}.pkl"
        return self.__dumper.load(cache_name) \
            if self.__dumper.has_cache(cache_name) and ignore_cache <= 1 \
            else self.__retrieve_disaster_types(country)

    def __make_country_disasters_dict(self, country_list, ignore_cache: int):
        country_disasters_dict = {}
        for country in country_list:
            disasters = self.__get_disasters(country, ignore_cache)
            logging.info(f"Adding disasters for {country.get_name()}")
            country_disasters_dict[country] = disasters
        return country_disasters_dict

    def __get_disaster_types_for_all_countries(self, ignore_cache: int):
        country_list = self.__dumper.load(CSVCrawler.COUNTRY_CACHE_FILE) \
            if self.__dumper.has_cache(CSVCrawler.COUNTRY_CACHE_FILE) \
            and ignore_cache <= 2 \
            else self.__retrieve_country_list()
        country_disasters_dict = \
            self.__make_country_disasters_dict(country_list, ignore_cache)
        self.__dumper.cache(country_disasters_dict,
                            CSVCrawler.DISASTERS_CACHE_FILE)
        return country_disasters_dict

    @staticmethod
    def __retrieve_disaster_tags(country: Country):
        logging.info(f"Retrieving disasters of {country.get_name()}")
        html_text = CSVCrawler.retrieve_html_text(country.get_url())
        soup = BeautifulSoup(html_text, "lxml")
        disaster_selection = soup.find("select", attrs={"name": "eventos"})
        raw_disasters = CSVCrawler.remove_newlines(disaster_selection.contents)
        return raw_disasters[1:]

    def __cache_disasters_for_country(self, disasters, country):
        cache_folder = self.__dumper.get_cache_folder()
        country_cache_folder = f"{cache_folder}/disasters"
        if not os.path.exists(country_cache_folder):
            os.makedirs(country_cache_folder)
        self.__dumper.cache(disasters,
                            f"disasters/{country.get_name()}_"
                            f"{country.get_country_code()}.pkl")

    def __retrieve_disaster_types(self, country: Country):
        disaster_tags = CSVCrawler.__retrieve_disaster_tags(country)
        disasters = Disasters(country)
        for disaster_tag in disaster_tags:
            name_en = disaster_tag.string.strip()
            query_key = disaster_tag['value']
            disasters.add_disaster(Disaster(name_en=name_en,
                                            query_key=query_key))
        disasters.rename_duplicate_disasters()
        self.__cache_disasters_for_country(disasters, country)
        return disasters

    @staticmethod
    def generate_url(country: Country, disaster: Disaster):
        base_url = "https://www.desinventar.net/DesInventar/" \
                   "stats_spreadsheet.jsp?bookmark=1&countrycode="
        middle_url = "&maxhits=100&lang=EN&logic=AND&sortby=0&frompage=" \
                     "/definestats.jsp&bSum=Y&_stat="
        query_data_stat = "fichas.fechano"
        latter_url = ",,&nlevels=1&_variables="
        wanted_data_types = "1,fichas.muertos,fichas.heridos," \
                            "fichas.desaparece,fichas.vivdest,fichas.vivafec," \
                            "fichas.damnificados,fichas.afectados," \
                            "fichas.reubicados,fichas.evacuados," \
                            "fichas.valorus,fichas.valorloc,fichas.nescuelas," \
                            "fichas.nhospitales,fichas.nhectareas," \
                            "fichas.cabezas,fichas.kmvias&_eventos= "
        return base_url + country.get_country_code() + middle_url + \
            query_data_stat + latter_url + wanted_data_types \
            + disaster.query_key

    @staticmethod
    def download_disaster_csv(country, disaster, saving_directory,
                              ignore_exist_databases=False):
        filepath = f"{saving_directory}/{disaster.name}.csv"
        if os.path.exists(filepath) and not ignore_exist_databases:
            logging.info(f"Exist: {filepath}, skip")
            return
        logging.info(f"Downloading: {filepath}")
        r = requests.get(CSVCrawler.generate_url(country, disaster))
        with open(filepath, 'wb') as f:
            f.write(r.content)
        time.sleep(0.1)

    def download_country_data(self, country, disasters,
                              ignore_exist_databases=False):
        saving_directory = f"{self.__target_dir}/" \
                           f"{CSVCrawler.DATABASES_DIRECTORY_NAME}/" \
                           f"{country.get_name()}_" \
                           f"{country.get_country_code()}"
        if not os.path.exists(saving_directory):
            os.makedirs(saving_directory)
        for disaster in disasters:
            CSVCrawler.download_disaster_csv(country, disaster,
                                             saving_directory,
                                             ignore_exist_databases)

    def __get_country_disaster_dict(self, ignore_cache):
        return self.__dumper.load(CSVCrawler.DISASTERS_CACHE_FILE) \
                if self.__dumper.has_cache(CSVCrawler.DISASTERS_CACHE_FILE) \
                and ignore_cache == 0 \
                else self.__get_disaster_types_for_all_countries(ignore_cache)

    def run(self, mode=0):
        """
        Run the crawler.

        Parameter:
            mode (int): an integer from 0 to 7, whose highest bit determines
                whether ignore existing spreadsheets and last two bits determine
                the level of ignoring of caches.

                Let `ignore_cache = mode & 0b011`
                If `ignore_cache` is greater than 0, the crawler will ignore
                cache in `caches/disasters.pkl`. If `ignore_cache` is greater
                than 1, the crawler will ignore cache in `caches/disasters.pkl`
                and `caches/disasters/*`. If `ignore_cache` is greater than 2,
                all caches will be ignored.
        """
        if mode not in range(8):
            raise ValueError("Wrong mode number, should be in 0-7")
        logging.basicConfig(level=logging.INFO)
        ignore_exist_databases = mode & 0b100 == 1
        ignore_cache = mode & 0b011
        country_disasters_dict = self.__get_country_disaster_dict(ignore_cache)
        for country, disasters in country_disasters_dict.items():
            self.download_country_data(country, disasters,
                                             ignore_exist_databases)
