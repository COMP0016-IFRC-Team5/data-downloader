from ._exec import start

__all__ = ["start_download"]


def start_download(target_dir, mode=0):
    start(target_dir, mode)
