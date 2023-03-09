from ._csv_crawler import CSVCrawler
from ._cleaner import start_clean

__all__ = ["start"]


def start(target_dir, mode=0):
    csv_crawler = CSVCrawler(target_dir)
    csv_crawler.run(mode)
    start_clean(target_dir)

