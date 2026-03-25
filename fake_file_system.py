FAKE_FS = {
    "C:\\tmp": ["dir1", "file1.txt"],
    "C:\\tmp\\dir1": ["file2.txt"],
}

FILES = {
    "C:\\tmp\\file1.txt",
    "C:\\tmp\\dir1\\file2.txt",
}

def fake_exists(path):
    return path in FAKE_FS or path in FILES


def fake_isdir(path):
    return path in FAKE_FS


def fake_listdir(path):
    return FAKE_FS.get(path, [])


def fake_isfile(path):
    return path in FILES

