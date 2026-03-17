import os
from typing import Iterator, Union


class PathWalker:
    """
    Manages a pathname to a directory.
    Includes commands that resemble 'cd' and 'ls'
    """

    def __init__(self, path: str) -> None:
        """
        Init a PathWalker instance.

        @param path (str): the path to create the instance to.
            if the path isn't absolute, it will auto-append it to the CWD.
        """
        self.path = os.path.abspath(os.path.expanduser(path))

        if not os.path.exists(self.path):
            raise NameError(f"Path ({self.path}) not found.")

        if not os.path.isdir(self.path):
            raise NotADirectoryError(f"Given path ({self.path}) is not a directory!")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.path}')"

    def __str__(self) -> str:
        return self.path

    def __getitem__(self, item: str) -> "PathWalker":
        """
        Access a subdirectory.

        @param item (str): Subdirectory name.

        @return: Instance pointing to the new path.
        """
        if not isinstance(item, str):
            raise TypeError(f"Expected string, received {type(item)}")

        return PathWalker(os.path.join(self.path, item))

    def __iter__(self) -> Iterator[str]:
        """
        Iterates over the first layer contents in the directory.

        @return: Iterator[str]- files and directories in given directory path.
        """
        return iter(os.listdir(self.path))


def recurse_file(directory: Union[str, PathWalker], indent: str = "") -> None:
    """
    Recursively print the files and directories in a path.

    @param directory (str | PathWalker): Path to traverse.
    @param indent (str): Indentation for nested files/folders. (irrelevant)
    """
    if isinstance(directory, str):
        directory = PathWalker(directory)

    for name in sorted(directory):
        full_path = os.path.join(directory.path, name)

        if os.path.isfile(full_path):
            print(f"{indent}- {name}")
        else:
            print(indent + name)
            recurse_file(full_path, f"{indent}  ")
