import sys
import os
from os import path

from . import TEST_DIR


def pytest_sessionstart():
    """
    put drivers dir into sys.path
    :return:
    """
    drivers_dir = path.join(TEST_DIR, 'drivers')
    os.environ['PATH'] += os.pathsep + drivers_dir
