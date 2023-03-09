import requests
import time
import os
from ._country_info import countries

base_url = "https://www.desinventar.net/DesInventar/download/DI_export_"


def main(target_dir):
    directory = f"{target_dir}/XMLdatabase"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i, (code, country) in enumerate(countries):
        new_url = base_url + code + ".zip"
        filename = f"{directory}/{code}_{country}.zip"
        print(i)
        print(country)
        if os.path.exists(filename):
            continue
        r = requests.get(new_url)
        with open(filename, 'wb') as f:
            f.write(r.content)
        time.sleep(0.1)
