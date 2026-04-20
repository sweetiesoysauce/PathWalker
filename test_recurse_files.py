import pytest
from pathwalker import PathWalker, recurse_files

@pytest.mark.parametrize(
    "path, expected",
    [
        ("home", "user\n    dir1\n        - file2.txt\n    - file1.txt\n"),
    ],
)
def test_recurse_file(capsys, path, expected) -> None:
    """Do: Recursively print files in mocked directory. Expect: output contains file names."""
    walker = PathWalker(path)
    recurse_files(walker)

    outputs = capsys.readouterr().out

    assert outputs == expected
