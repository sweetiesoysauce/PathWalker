import pytest
from pathwalker import PathWalker

@pytest.mark.parametrize(
    "path, expected",
    [
        ("home\\user", "home\\user"),
        ("home\\user\\dir1", "home\\user\\dir1"),

        ("dir1", "home\\user\\dir1"),
        ("dir1\\dir3", "home\\user\\dir1\\dir3"),

        ("\\", "home\\user"),
        ("\\dir1", "home\\user\\dir1"),

        ("~", "home\\user"),
        ("~\\dir1", "home\\user\\dir1"),
        ("home\\user\\dir1\\..", "home\\user"),
        ("home\\user\\.", "home\\user"),
    ],
)
def test_init_valid(path, expected) :
    """
    Do: Initialize PathWalker with valid paths.
    Expect: path stored correctly.
    """
    assert PathWalker(path).path == expected


@pytest.mark.parametrize(
    "path, expected_exception, expected_string",
    [
        ("does_not_exist", NameError, "Path (home\\user\\does_not_exist) not found."),
        ("home\\user\\dir1\\file2.txt", NotADirectoryError,
         "Given path (home\\user\\dir1\\file2.txt) is not a directory!"),
        (123, TypeError, "Expected string, got int"),
        ("home\\..", NameError, "Path (.) not found."),
    ],
)
def test_init_invalid(path, expected_exception, expected_string) :
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
        ("dir1", "PathWalker('home\\user\\dir1')"),
        ("~", "PathWalker('home\\user')"),
    ],
)
def test_repr(path, expected) :
    """
    Do: Convert PathWalker to string representations.
    Expect: correct output for repr.
    """
    assert repr(PathWalker(path)) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("\\", "home\\user"),
        ("dir1", "home\\user\\dir1"),
        ("~", "home\\user"),
    ],
)
def test_str(path, expected) :
    """
    Do: Convert PathWalker to string representations.
    Expect: correct output for str.
    """
    assert str(PathWalker(path)) == expected


@pytest.mark.parametrize(
    "path, item, expected",
    [
        ("\\", "dir1", "home\\user\\dir1"),
        ("home\\user\\dir1\\..", "dir1", "home\\user\\dir1"),

        ("home\\user", ".", "home\\user"),
        ("home\\user\\dir1", "..", "home\\user"),
        ("home\\user\\dir1", "..\\dir4", "home\\user\\dir4"),
    ],
)
def test_get_item_valid(path, item, expected) :
    """
    Do: Access subdirectory using getitem.
    Expect: correct PathWalker path.
    """
    new_path = PathWalker(path)[item]
    assert new_path.path == expected


@pytest.mark.parametrize(
    "path, item, expected_exception, expected_string",
    [
        ("\\", 123, TypeError, "join() argument must be str or bytes, not 'int'"),
        ("\\", None, TypeError, "join() argument must be str or bytes, not 'NoneType'"),
        ("\\", 5.5, TypeError, "join() argument must be str or bytes, not 'float'"),
        ("\\", "nonexistent", NameError, "Path (home\\user\\nonexistent) not found."),
        ("\\", "..\\..", NameError, "Path (.) not found.")
    ],
)
def test_get_item_invalid(path, item, expected_exception, expected_string) :
    """
    Do: Access with invalid key types.
    Expect: TypeError raised.
    """
    with pytest.raises(expected_exception) as execinfo:
        PathWalker(path)[item]

    assert str(execinfo.value) == expected_string



@pytest.mark.parametrize(
    "path, expected",
    [
        ("\\", ["dir1", "dir4", "file1.txt"]),
        ("home\\user\\dir1", ["dir3", "file2.txt"]),
        ("home\\user\\dir1\\..", ["dir1", "dir4", "file1.txt"]),
    ],
)
def test_iter(path, expected) :
    """
    Do: Iterate over directory contents.
    Expect: correct list of files/directories.
    """
    files = list(PathWalker(path))
    assert sorted(files) == sorted(expected)
