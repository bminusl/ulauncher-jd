import os

from . import BASEDIR
from .format import match_type


def search(query):
    query = query.lower()

    for root, dirs, files in os.walk(BASEDIR):

        depth = root.count(os.sep) - BASEDIR.count(os.sep)

        for name in dirs:
            if query in name.lower():
                try:
                    component_type = ["area", "category", "id"][depth]
                except IndexError:
                    pass
                else:
                    yield component_type, os.path.join(root, name)


def find_name(number):
    desired_type = match_type(number)
    for result_type, result_abspath in search(number):
        if result_type == desired_type:
            return os.path.basename(result_abspath)
