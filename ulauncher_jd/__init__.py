from collections import namedtuple

ComponentInfo = namedtuple(
    "ComponentInfo", ("type", "abspath", "number", "number_data")
)


# TEMPORARY FOR NOW, DEBUGGING
BASEDIR = "/tmp/jd"
BASEDIR_INFO = ComponentInfo(None, BASEDIR, None, None)
