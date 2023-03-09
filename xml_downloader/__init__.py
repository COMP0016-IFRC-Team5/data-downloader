from ._main import start
__all__ = ["start_process"]


def start_process(target_dir, clean_zip=False):
    start(target_dir, clean_zip)
