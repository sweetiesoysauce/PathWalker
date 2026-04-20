import pytest
from unittest.mock import Mock

FAKE_FS = {
    "home": {
        "user": {
            "dir1": {
                "file2.txt": None,
            },
            "file1.txt": None,
        }
    },
    "dir2": {},
    "file3": None,
}

HOME = ["home", "user"]

def _walk(path: str):
    parts = fake_abspath(fake_expanduser(path)).split("\\")
    node = FAKE_FS

    for part in parts:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return False

    return node

def fake_expanduser(path):

    if path.startswith("~"):
        path = "\\".join(HOME) + path[1:]

    return path

def fake_abspath(path):
    parts = path.split("\\")

    if path.startswith("\\"):
        parts = HOME + parts[1:]

    normalized = []
    for part in parts:
        if part in ("", "."):
            continue
        elif part == "..":
            if normalized:
                normalized.pop()
        else:
            normalized.append(part)

    return "\\".join(normalized)
def fake_exists(path):
    return _walk(path) is not False


def fake_isdir(path):
    node = _walk(path)
    return isinstance(node, dict)


def fake_isfile(path):
    node = _walk(path)
    return node is None


def fake_listdir(path):
    node = _walk(path)

    if node is None:
        raise FileNotFoundError(path)

    if not isinstance(node, dict):
        raise NotADirectoryError(path)

    return list(node.keys())

@pytest.fixture(autouse=True)
def os_patches(mocker):
    mocker.patch("pathwalker.os.path.exists", side_effect=fake_exists)
    mocker.patch("pathwalker.os.path.isdir", side_effect=fake_isdir)
    mocker.patch("pathwalker.os.path.isfile", side_effect=fake_isfile)
    mocker.patch("pathwalker.os.listdir", side_effect=fake_listdir)
    mocker.patch("pathwalker.os.path.abspath", side_effect=fake_abspath)
    mocker.patch("pathwalker.os.path.expanduser", side_effect=fake_expanduser)
