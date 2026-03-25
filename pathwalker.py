import os
from typing import Iterator, Union

TAB = "    "

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
        if not isinstance(path, str):
            raise TypeError(f"Expected string, got {type(path).__name__}")

        self.path = os.path.abspath(os.path.expanduser(path))

        if not os.path.exists(self.path):
            raise NameError(f"Path ({self.path}) not found.")

        if not os.path.isdir(self.path):
            raise NotADirectoryError(f"Given path ({self.path}) is not a directory!")

    def __repr__(self) -> str:
        """
        Represents the class and its variables for debugging.

        @return: A debugging string containing class name and current path.
        """
        return f"{self.__class__.__name__}('{self.path}')"

    def __str__(self) -> str:
        """
        Converts the variable to a readable string.

        @return: A string containing the current path.
        """
        return self.path

    def __getitem__(self, item: str) -> "PathWalker":
        """
        Access a subdirectory.

        @param item (str): Subdirectory name.

        @return: Instance pointing to the new path.
        """

        return PathWalker(os.path.join(self.path, item))

    def __iter__(self) -> Iterator[str]:
        """
        Iterates over the first layer contents in the directory.

        @return: Iterator[str]- files and directories in given directory path.
        """
        return iter(os.listdir(self.path))


def recurse_files(directory: Union[str, PathWalker], indent: int = 0) -> None:
    """
    Recursively print the files and directories in a path.

    @param directory (str | PathWalker): Path to traverse.
    @param indent (str): Indentation for nested files/folders. (irrelevant)
    """
    directory = PathWalker(directory) if isinstance(directory, str) else directory


    for name in directory:
        full_path = os.path.join(directory.path, name)

        if os.path.isfile(full_path):
            print(f"{indent * TAB}- {name}")
        else:
            print(f"{indent * TAB} {name}")
            recurse_files(PathWalker(full_path), ++indent)
