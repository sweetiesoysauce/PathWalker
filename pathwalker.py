
import os
from typing import Iterator


class PathWalker:
    def __init__(self, path: str) -> None:
        """
        Init a PathWalker instance.

        @param path (str): the path to create the instance to.
            if the path isn't absolute, it will auto-append it to the CWD.
        """
        path = os.path.expanduser(path)
        path = os.path.abspath(path)
        path = os.path.normpath(path)

        if not os.path.exists(path):
            raise NameError(f"Path ({path}) not found.")

        if not os.path.isdir(path):
            raise NotADirectoryError(f"Given path ({path}) is not a directory!")

        self.path = path
        self._current_index = -1

    def __repr__(self) -> str:
        return f"PathWalker('{self.path}')"

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

        new_path = os.path.join(self.path, item)
        return PathWalker(new_path)

    def __iter__(self) -> Iterator[str]:
        self._current_index = -1
        return self

    def __next__(self) -> str:
        listdir = os.listdir(self.path)

        if (len(listdir) - 1) == self._current_index:
            raise StopIteration

        self._current_index += 1
        return listdir[self._current_index]
