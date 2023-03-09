import record_converter


if __name__ == '__main__':
    converter = record_converter.RecordsConverter()
    converter.set_data_folder("./data")
    converter.start_conversion()
