from collections import namedtuple

ComponentInfo = namedtuple(
    "ComponentInfo", ("type", "abspath", "number", "number_data")
)

# A dummy singleton object to pass information
preferences = {}
