import os
import tempfile


def temp_file(suffix='') -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return path
