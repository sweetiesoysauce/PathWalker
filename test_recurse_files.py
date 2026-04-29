import pytest
from pathwalker import PathWalker, recurse_files

@pytest.mark.parametrize(
    "path, expected",
    [
        ("home",
         "user\n"
         "    dir1\n"
         "        dir3\n"
         "        - file2.txt\n"
         "    - file1.txt\n"
         "    dir4\n"),
    ],
)

def test_recurse_file_with_string(capsys, path, expected) :
    """Test recurse_files with string input."""
    recurse_files(path)
    output = capsys.readouterr().out
    assert output == expected


def test_recurse_file_with_pathwalker(capsys) :
    """Test recurse_files with PathWalker input."""
    walker = PathWalker("home")
    recurse_files(walker)
    output = capsys.readouterr().out
    assert "file1.txt" in output


@pytest.mark.parametrize(
    "bad_input",
    [123, None, 5.5],
)
def test_recurse_file_invalid_input(bad_input) :
    """Test recurse_files with invalid input."""
    with pytest.raises(TypeError) :
        recurse_files(bad_input)
