# pylint: disable=missing-docstring

import yaml
import copy
import re

from colorama import Fore, Style

from kampai.conf.conf_struct import ConfStruct


class ConfLoader():
    """
    loads project and defaults yaml configuration files
    and provides a validated configuration object
    allows the objects consuming the configuration
    to easilly access the conf parameters in nested objects attributes
    """

    def __init__(self, project_conf_path, defaults_conf_path):
        """
        loads configuration from project and defaults yaml files
        processes validated conf
        """

        self.project_conf = self.__load_yaml_conf(project_conf_path)
        self.defaults_conf = self.__load_yaml_conf(defaults_conf_path)
        self.conf = copy.deepcopy(self.defaults_conf)
        self.__validate_conf(self.project_conf, self.conf)

    def __repr__(self):
        """
        returns a diff of repr between conf from project and defaults
        conf present only in defaults is highlighted in magenta
        conf present only in project is highlighted in cyan
        """

        # getting representation of project, defaults and validated conf
        project_repr = repr(self.project_conf).split('\n')
        defaults_repr = repr(self.defaults_conf).split('\n')
        conf_repr = repr(self.conf).split('\n')

        # showing representation of validated configuration
        representation = []

        for conf_line in conf_repr:

            # checking if line is shared
            line_in_project = conf_line in project_repr
            line_in_defaults = conf_line in defaults_repr

            # appending representation
            if line_in_defaults:

                # check if line is in project
                if line_in_project:

                    # line present both in project and defaults
                    representation.append(Fore.BLUE + conf_line
                                          + Style.RESET_ALL)
                else:

                    # line present only in defaults
                    representation.append(conf_line)
            else:

                # get conf from line
                conf = re.search(r"^[a-zA-Z][\w\.]*", conf_line).group(0)

                # check if line conf is in defaults
                if self.defaults_conf.has_conf(conf):

                    # line present in defaults and customized in project
                    representation.append(Fore.CYAN + conf_line
                                          + Style.RESET_ALL)
                else:

                    # line present only in project
                    representation.append(Fore.MAGENTA + conf_line
                                          + Style.RESET_ALL)

        return "\n".join(representation)

    def __load_yaml_conf(self, file_path):

        # yaml allows to benefit from an organised structure (a dictionary)
        # allowing to pass the conf to the consuming objects
        # conversion to the ConfStruct class allows
        # to access easilly conf elements using the dot notation

        # load conf file
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)

        # convert conf dictionary into ConfStruct object
        conf = ConfStruct(**config)

        return conf

    def __validate_conf(self, project_conf, defaults_conf):
        """
        processes conf object by iterating through defaults conf object
        and replacing values by project conf values when available
        """

        # iterate through defaults conf object
        for key, value in defaults_conf.__dict__.items():

            # checking whether key contains conf struct
            if isinstance(value, ConfStruct):

                # retrieve corresponding project conf
                if hasattr(project_conf, key):

                    # iterate recursively through conf struct representation
                    self.__validate_conf(getattr(project_conf, key), value)

            else:

                # validate other datatypes against project conf
                if hasattr(project_conf, key):

                    # validate project conf data type
                    if type(getattr(project_conf, key)) == type(value):

                        # replace defaults value with project value
                        setattr(defaults_conf, key, getattr(project_conf, key))

                    else:

                        # generate warning
                        print(Fore.RED
                              + "⚠️  invalid data type inside project conf "
                              + f"file for key '{key}' value '{value}', "
                              + "conf line is ignored"
                              + Style.RESET_ALL)

        # handle additional confs from project
        for key, value in project_conf.__dict__.items():

            # checking whether key exists in defaults
            if not hasattr(defaults_conf, key):

                # setting missing key
                setattr(defaults_conf, key, getattr(project_conf, key))
