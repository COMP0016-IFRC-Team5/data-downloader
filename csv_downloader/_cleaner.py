import os
from glob import glob
from pathlib import Path

__all__ = ["start_clean"]

SOURCE_DIRECTORY_NAME = "raw_csv_files"
OUTPUT_DIRECTORY_NAME = "cleaned_databases"
TARGET_DIRECTORY = None
DATABASES_FOLDER = None
CLEANED_FOLDER = None


def clean_file_contents(contents: list[str]):
    return contents[4:-2]


def clean_all_databases():
    database_files = glob(f"{DATABASES_FOLDER}/**/*.csv")
    for raw_data_file in database_files:
        target_directory = os.path.dirname(raw_data_file).replace(
            SOURCE_DIRECTORY_NAME, OUTPUT_DIRECTORY_NAME)
        target_file = raw_data_file.replace(SOURCE_DIRECTORY_NAME,
                                            OUTPUT_DIRECTORY_NAME)
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        with open(raw_data_file, 'r') as source:
            with open(target_file, 'w') as destination:
                destination.writelines(clean_file_contents(source.readlines()))


def remove_empty_databases():
    cleaned_data_files = glob(f"{CLEANED_FOLDER}/**/*.csv")
    for cleaned_data_file in cleaned_data_files:
        delete = False
        with open(cleaned_data_file, 'r') as f:
            if len(f.readlines()) < 2:
                delete = True
        if delete:
            Path(cleaned_data_file).unlink()


def start_clean(target_dir: str):
    global TARGET_DIRECTORY, DATABASES_FOLDER, CLEANED_FOLDER
    TARGET_DIRECTORY = target_dir
    DATABASES_FOLDER = f"{TARGET_DIRECTORY}/{SOURCE_DIRECTORY_NAME}"
    CLEANED_FOLDER = f"{TARGET_DIRECTORY}/{OUTPUT_DIRECTORY_NAME}"
    print(f"Cleaning databases in {DATABASES_FOLDER} and saving them to "
          f"{CLEANED_FOLDER}...")
    clean_all_databases()
    remove_empty_databases()
