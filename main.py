import os
from pathwalker import PathWalker


def recurse_file(directory, indent: str = "") -> None:
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
            print(indent + "- " + name)
        else:
            print(indent + "+ " + name)
            recurse_file(PathWalker(full_path), indent + "   ")


def main() -> None:
    walker = PathWalker("C:\\Users\\Ela\\AppData\\Local\\Programs\\Python\\Python38")
    recurse_file(walker)

if __name__ == "__main__":
    main()
