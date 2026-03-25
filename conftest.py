import pytest
from fake_file_system import fake_isdir, fake_exists, fake_listdir, fake_isfile


@pytest.fixture(autouse=True)
def os_patches(mocker):
    mocker.patch("pathwalker.os.path.exists", side_effect=fake_exists)
    mocker.patch("pathwalker.os.path.isdir", side_effect=fake_isdir)
    mocker.patch("pathwalker.os.listdir", side_effect=fake_listdir)
    mocker.patch("pathwalker.os.path.isfile", side_effect=fake_isfile)

