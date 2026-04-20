import pytest

from pathwalker import PathWalker


@pytest.mark.parametrize(
    "path, expected",
    [
        ("~", "home\\user"),
        ("home\\user\\dir1\\..", "home\\user"),
        ("home\\user\\.", "home\\user")
    ],
)
def test_init_valid(path, expected) -> None:
    """
    Do: Initialize PathWalker with valid paths.
    Expect: path stored correctly.
    """
    assert PathWalker(path).path == expected


@pytest.mark.parametrize(
    "path, expected_exception, expected_string",
    [
        ("does_not_exist", NameError, "Path (does_not_exist) not found."),
        ("home\\user\\dir1\\file2.txt", NotADirectoryError, "Given path (home\\user\\dir1\\file2.txt) is not a directory!"),
        (123, TypeError, "Expected string, got int"),
        ("home\\..", NameError, "Path () not found.")
    ],
)
def test_init_invalid(path, expected_exception, expected_string) -> None:
    """
    Do: Initialize PathWalker with invalid paths.
    Expect: correct exception is raised.
    """
    with pytest.raises(expected_exception) as execinfo:
        PathWalker(path)

    assert str(execinfo.value) == expected_string

@pytest.mark.parametrize(
    "path, expected",
    [
        ("\\", "PathWalker('home\\user')"),
    ],
)
def test_repr(path, expected) -> None:
    """
    Do: Convert PathWalker to string representations.
    Expect: correct output for repr and str.
    """
    assert repr(PathWalker(path)) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("\\", "home\\user"),
    ],
)
def test_str(path, expected) -> None:
    """
        Do: Convert PathWalker to string representations.
        Expect: correct output for repr and str.
        """
    assert str(PathWalker(path)) == expected


@pytest.mark.parametrize(
    "path, item, expected",
    [
        ("\\", "dir1", "home\\user\\dir1"),
        ("home\\user\\dir1\\..", "dir1", "home\\user\\dir1")
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
    [("\\", 123),
     ("\\", None),
     ("\\", 5.5),
     ("\\", "error")],
)
def test_get_item_invalid_type(path, item) -> None:
    """
    Do: Access with invalid key types.
    Expect: TypeError raised.
    """
    with pytest.raises((TypeError, KeyError, NameError)):
        PathWalker(path)[item]


@pytest.mark.parametrize(
    "path, expected",
    [
        ("\\", ["dir1", "file1.txt"]),
    ],
)
def test_iter(path, expected) -> None:
    """
    Do: Iterate over directory contents.
    Expect: correct list of files/directories.
    """
    files = list(PathWalker(path))
    assert sorted(files) == sorted(expected)
