# pylint: disable=missing-docstring

from kampai.conf.conf_loader import ConfLoader

from colorama import Fore, Style

from os.path import join, dirname


def load_conf():

    # load conf
    print(Fore.GREEN + "\nLoading configuration..."
          + Style.RESET_ALL)

    conf_path = dirname(__file__)
    project_conf_path = join(conf_path, "app.yaml")
    defaults_conf_path = join(conf_path, "app.defaults.yaml")
    conf_loader = ConfLoader(project_conf_path, defaults_conf_path)
    conf = conf_loader.conf

    print(Fore.GREEN + "\nLoaded configuration:"
          + Style.RESET_ALL
          + str(conf_loader))

    return conf
