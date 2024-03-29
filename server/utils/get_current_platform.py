import os


def get_os():
    platform = os.name
    if platform == 'nt':
        return 'Windows'
    elif platform == 'posix':
        from sys import platform as _platform
        if _platform == 'darwin':
            return 'macOS'
        elif _platform == 'linux' or _platform == 'linux2':
            return 'Linux'
    return 'Unknown'
