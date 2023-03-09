import os

from ._file import File

__all__ = ["Directory"]


class Directory:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError("folder does not exist")
        self.__path = path if path != "" and path[-1] != '/' else path[:-1]
        self.__dirname = os.path.basename(path)
        self.__files: list[File] = []
        self.__directories: list[Directory] = []
        self.__content_names: list[str] = []
        self.__update()

    def __scan_directory(self):
        with os.scandir(self.__path) as it:
            for entry in it:
                if entry.is_file():
                    self.__files.append(File(entry.path))
                elif entry.is_dir():
                    self.__directories.append(Directory(entry.path))

    def __update(self):
        self.__scan_directory()
        self.__files.sort(key=lambda f: f.get_filename())
        self.__directories.sort(key=lambda d: d.get_dirname())
        self.__content_names = list(
            map(lambda c: c.get_dirname() if isinstance(c, Directory)
                else c.get_filename(),
                self.get_contents()))

    def get_directories(self):
        return self.__directories

    def get_files(self):
        return self.__files

    def get_all_files(self):
        files: list[File] = []
        files.extend(self.__files)
        for d in self.__directories:
            files.extend(d.get_files())
        return files

    def find_directory(self, directory: str):
        return next(
            (d for d in self.__directories if d.get_dirname() == directory),
            None
        )

    def find_file(self, file: str):
        return next((f for f in self.__files if f.get_filename() == file), None)

    def create_subdirectory(self, directory):
        path = f"{self.__path}/{directory}"
        if os.path.exists(path):
            return
        os.makedirs(path)
        self.__update()

    def get_contents(self):
        contents = []
        contents.extend(self.__files)
        contents.extend(self.__directories)
        return contents

    def get_content_names(self):
        return self.__content_names

    def get_dirname(self):
        return self.__dirname

    def get_path(self):
        return self.__path
