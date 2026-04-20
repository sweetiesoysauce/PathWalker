import pytest
from pathwalker import PathWalker, recurse_files

@pytest.mark.parametrize(
    "path, expected",
    [
        ("\\tmp", "file1"),
    ],
)
def test_recurse_file(capsys, os_patches, path, expected) -> None:
    """Do: Recursively print files in mocked directory. Expect: output contains file names."""
    walker = PathWalker(path)
    recurse_files(walker)
    output = capsys.readouterr().out
    assert expected in output
