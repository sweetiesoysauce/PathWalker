from unittest.mock import patch

import pytest

from pathwalker import PathWalker


# __init__ tests
def test_init_valid() -> None:
    """Do: Initialize PathWalker with valid path. Expect: path stored correctly."""
    with patch("pathwalker.os.path.exists", return_value=True), \
         patch("pathwalker.os.path.isdir", return_value=True):
        walker = PathWalker("\\tmp")
        assert walker.path == "C:\\tmp"


def test_init_path_not_found() -> None:
    """Do: Initialize PathWalker with non-existent path. Expect: NameError raised."""
    with patch("pathwalker.os.path.exists", return_value=False):
        with pytest.raises(NameError):
            PathWalker("fake")


def test_init_not_dir() -> None:
    """Do: Initialize PathWalker with file path. Expect: NotADirectoryError raised."""
    with patch("pathwalker.os.path.exists", return_value=True), \
         patch("pathwalker.os.path.isdir", return_value=False):
        with pytest.raises(NotADirectoryError):
            PathWalker("fake")


# representation tests
def test_repr() -> None:
    """Do: Check __repr__ returns correct string."""
    with patch("pathwalker.os.path.exists", return_value=True), \
         patch("pathwalker.os.path.isdir", return_value=True):
        walker = PathWalker("/tmp")
        assert repr(walker) == "PathWalker('C:\\tmp')"


def test_str() -> None:
    """Do: Check __str__ returns path string."""
    with patch("pathwalker.os.path.exists", return_value=True), \
         patch("pathwalker.os.path.isdir", return_value=True):
        walker = PathWalker("/tmp")
        assert str(walker) == "C:\\tmp"


# navigation tests
def test_get_item() -> None:
    """Do: Access subdirectory via __getitem__. Expect: PathWalker instance with correct path."""
    with patch("pathwalker.os.path.exists", return_value=True), \
         patch("pathwalker.os.path.isdir", return_value=True):
        walker = PathWalker("\\tmp")
        new_path = walker["test"]
        assert new_path.path == "C:\\tmp\\test"


def test_get_item_invalid_type() -> None:
    """Do: Access with non-string key. Expect: TypeError raised."""
    with patch("pathwalker.os.path.exists", return_value=True), \
         patch("pathwalker.os.path.isdir", return_value=True):
        walker = PathWalker("\\tmp")
        with pytest.raises(TypeError):
            walker[123]


def test_iter() -> None:
    """Do: Iterate over directory contents. Expect: returns sorted list."""
    with patch("pathwalker.os.path.exists", return_value=True), \
         patch("pathwalker.os.path.isdir", return_value=True), \
         patch("pathwalker.os.listdir", return_value=["one", "two"]):
        walker = PathWalker("\\tmp")
        files = list(walker)
        assert files == ["one", "two"]
