from ._csv_crawler import CSVCrawler

__all__ = ["start"]


def start(target_dir, mode=0):
    csv_crawler = CSVCrawler(target_dir)
    csv_crawler.run(mode)
