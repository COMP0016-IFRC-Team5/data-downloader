import zipfile
import shutil

import requests
import time
import os
from sys import stdout

from ._country_info import countries

__all__ = ["start"]

base_url = "https://www.desinventar.net/DesInventar/download/DI_export_"


def download(target_dir):
    directory = f"{target_dir}/zip_files"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i, (code, country) in enumerate(countries.items()):
        new_url = base_url + code + ".zip"
        filename = f"{directory}/{code}_{country}.zip"
        message = f"{i+1} - {code} - {country}"
        if os.path.exists(filename):
            message += " - Already downloaded"
            print(message)
            continue
        stdout.write(f"{message} - Downloading...")
        stdout.flush()
        r = requests.get(new_url)
        with open(filename, 'wb') as f:
            f.write(r.content)
        stdout.write('\x1b[2K')
        stdout.write(f"\r{message} - Done!\n")
        time.sleep(0.1)


def extract(target_dir):
    source_directory = f"{target_dir}/zip_files"
    output_directory = f"{target_dir}/extracted_files"
    if not os.path.exists(source_directory):
        raise FileNotFoundError("No zip files found")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for i, (code, country) in enumerate(countries.items()):
        filename = f"{source_directory}/{code}_{country}.zip"
        if not os.path.exists(filename):
            print(f"File {code}_{country}.zip not found")
            continue
        stdout.write(f"{i+1} - {code} - {country} - Extracting...")
        stdout.flush()
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(f"{output_directory}/{code}_{country}")
        stdout.write('\x1b[2K')
        stdout.write(f"\r{i+1} - {code} - {country} - Done!\n")


def move(target_dir):
    source_directory = f"{target_dir}/extracted_files"
    output_directory = f"{target_dir}/XMLdatabases"
    if not os.path.exists(source_directory):
        raise FileNotFoundError("No extracted files found")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for i, (code, country) in enumerate(countries.items()):
        filename = f"{source_directory}/{code}_{country}/DI_export_{code}.xml"
        if not os.path.exists(filename):
            print(f"File {code}_{country}.xml not found")
            continue
        os.rename(filename, f"{output_directory}/{country}.xml")


def clean(target_dir, clean_zip=False):
    source_directory = f"{target_dir}/extracted_files"
    zip_directory = f"{target_dir}/zip_files"
    try:
        shutil.rmtree(source_directory)
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")

    if clean_zip:
        try:
            shutil.rmtree(zip_directory)
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")


def start(target_dir, clean_zip=False):
    download(target_dir)
    extract(target_dir)
    move(target_dir)
    clean(target_dir, clean_zip)
