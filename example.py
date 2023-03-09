import xml_downloader
import csv_downloader
import record_converter
import categoriser


if __name__ == '__main__':
    target_dir = "./data"
    xml_downloader.start_process(target_dir=target_dir, clean_zip=False)
    csv_downloader.start_download(target_dir, mode=0b111)

    converter = record_converter.RecordsConverter()
    converter.set_data_folder(target_dir)
    converter.start_conversion()

    categoriser.start_categorise(target_dir)
