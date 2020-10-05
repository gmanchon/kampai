
from colorama import Fore, Style

import os

COMMIT_SIGNATURE = "kampai 🎉 🍰"  # identifies a kampai project


def is_cwd_within_generated_project(print_error_if_not_within=False):
    """
    checks whether the current working directory is a git repo
    that was generated using kampai by verifying that the first commit
    contains the kampai commit signature
    """

    # retrieving first commit of current working directory
    # git log --oneline returns one commit per line
    # 2>/dev/null eliminates errors but not the standard output,
    # which is read by os.popen
    # tail -1 retrieves the first commit of the git repo
    git_log_cmd = "git log --oneline 2>/dev/null " \
                  " | tail -1"

    git_first_commit = os.popen(git_log_cmd).read()

    # checking whether first commit was performed by kampai
    if COMMIT_SIGNATURE not in git_first_commit:
        if print_error_if_not_within:
            print(Fore.RED + "This command needs to be run "
                  "within a kampai generated project... 😅"
                  + Style.RESET_ALL)

        return False

    return True


def get_generated_project_top_level():
    """
    retrieves the top level of the generated kampai project
    which corresponds to the top level of the git repository
    """

    # getting git repo top level
    get_root_cmd = "git rev-parse --show-toplevel"

    root_path = os.popen(get_root_cmd).read().strip()

    if root_path == "":
        print(Fore.RED + "Error getting git repo top level: %s (%s) 😢"
              % (root_path, get_root_cmd)
              + Style.RESET_ALL)

        exit(1)

    return root_path


def get_package_name():
    """
    retrieves project package name from setup.py
    """

    # getting git repo top level
    project_root = get_generated_project_top_level()
    get_name_cmd = "cd %s " \
                   " && cat setup.py | grep 'setup(name=\"'" \
                   % project_root

    name = os.popen(get_name_cmd).read().strip("setup(name=")
    name = name.strip().strip(',').strip('"')

    if name == "":
        print(Fore.RED + "Error getting package name: %s (%s) 😢"
              % (name, get_name_cmd)
              + Style.RESET_ALL)

        exit(1)

    return name
