from os import path

TEST_DIR = path.dirname(path.abspath(__file__))
DATA_DIR = path.join(TEST_DIR, 'data')


def get_data_file_path(file_name):
    return path.join(DATA_DIR, file_name)
