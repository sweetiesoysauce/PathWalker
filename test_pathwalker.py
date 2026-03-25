import pytest

from pathwalker import PathWalker


# ---------- INIT TESTS ----------

@pytest.mark.parametrize(
    "path, expected",
    [
        ("\\tmp", "C:\\tmp"),
    ],
)
def test_init_valid(path, expected) -> None:
    """
    Do: Initialize PathWalker with valid paths.
    Expect: path stored correctly.
    """
    walker = PathWalker(path)
    assert walker.path == expected


@pytest.mark.parametrize(
    "path, expected_exception",
    [
        ("does_not_exist", NameError),
        ("C:\\tmp\\dir1\\file2.txt", NotADirectoryError),
    ],
)
def test_init_invalid(path, expected_exception) -> None:
    """
    Do: Initialize PathWalker with invalid paths.
    Expect: correct exception is raised.
    """
    with pytest.raises(expected_exception):
        PathWalker(path)


# ---------- REPRESENTATION TESTS ----------

@pytest.mark.parametrize(
    "path, func, expected",
    [
        ("\\tmp", repr, "PathWalker('C:\\tmp')"),
        ("\\tmp", str, "C:\\tmp"),
    ],
)
def test_representation(path, func, expected) -> None:
    """
    Do: Convert PathWalker to string representations.
    Expect: correct output for repr and str.
    """
    assert func(PathWalker(path)) == expected


# ---------- GETITEM TESTS ----------

@pytest.mark.parametrize(
    "path, item, expected",
    [
        ("\\tmp", "dir1", "C:\\tmp\\dir1"),
    ],
)
def test_get_item_valid(path, item, expected) -> None:
    """
    Do: Access subdirectory using getitem.
    Expect: correct PathWalker path.
    """
    new_path = PathWalker(path)[item]
    assert new_path.path == expected


@pytest.mark.parametrize(
    "path, item",
    [("\\tmp", 123),
     ("\\tmp", None),
     ("\\tmp", 5.5)],
)
def test_get_item_invalid_type(path, item) -> None:
    """
    Do: Access with invalid key types.
    Expect: TypeError raised.
    """
    with pytest.raises(TypeError):
        PathWalker(path)[item]


# ---------- ITER TESTS ----------

@pytest.mark.parametrize(
    "path, expected",
    [
        ("\\tmp", ["dir1", "file1.txt"]),
    ],
)
def test_iter(path, expected) -> None:
    """
    Do: Iterate over directory contents.
    Expect: correct list of files/directories.
    """
    files = list(PathWalker(path))
    assert sorted(files) == sorted(expected)
