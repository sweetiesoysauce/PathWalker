from unittest.mock import patch

from main import recurse_file
from pathwalker import PathWalker


def test_recurse_file(capsys) -> None:
    """Do: Recursively print files in mocked directory. Expect: output contains file names."""
    with patch("pathwalker.os.path.exists", return_value=True), \
         patch("pathwalker.os.path.isdir", return_value=True), \
         patch("pathwalker.os.listdir", return_value=["one", "two"]), \
         patch("main.os.path.isfile", return_value=True):
        walker = PathWalker("/tmp")
        recurse_file(walker)
        output = capsys.readouterr().out
        assert "one" in output
        assert "two" in output
