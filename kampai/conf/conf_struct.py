# pylint: disable=missing-docstring

from collections.abc import Mapping


# https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
class ConfStruct:
    """
    converts a dictionary into nested objects having attributes
    containing the values of the dictionary
    given `d = { "a": { "b": { "c": True, "d": [1, 2, 3], "e": ", "f": 5 } } }`
    `s = ConfStruct(**d)` allows to access conf using the dot notation `s.a.b.d`
    """

    def __init__(self, **entries):
        """
        iterates through the provided dictionary
        non mapping data types are stored in instance variables
        mapping data types are stored as conf structs in instance variables
        """

        # convert dictionary parameter into nested objects and attributes
        for key, value in entries.items():

            # checking whether key contains a dictionary
            if isinstance(value, Mapping):

                # iterate recursively through sub dictionary
                # and store resulting object into structure
                self.__dict__[key] = ConfStruct(**value)

            else:

                # other datatypes are stored as provided
                # into the structure
                self.__dict__[key] = value

    def __repr__(self):
        """
        builds a visual representation of the loaded data
        using the example in the initializer:
        `a.b.c = True
        a.b.d = [1, 2, 3]
        a.b.e = ''
        a.b.f = 5`
        """

        representation = ""

        # iterate through instance variables
        for key, value in self.__dict__.items():

            # checking whether key contains conf struct
            if isinstance(value, ConfStruct):

                # iterate recursively through conf struct representation
                representation += f"\n{key}.".join(repr(value).split("\n"))

            else:

                # other datatypes are displayed using default repr
                representation += f"\n{key} = {repr(value)}"

        return representation

    def has_conf(self, conf):
        """
        checks whether object contains chain of attributes
        described by conf parameter such as `a.b.c`
        """

        # get list of attributes in chain
        attributes = conf.split('.')

        # iterate through objects
        current_object = self

        for attribute in attributes:

            # check if current object has attribute
            if not hasattr(current_object, attribute):
                return False

            # update current object
            current_object = getattr(current_object, attribute)

        return True
