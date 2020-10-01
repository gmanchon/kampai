
from colorama import Fore, Style

import os


def is_cwd_within_generated_project(print_error_if_not_within=False):
    """
    checks whether the current working directory is a git repo
    that was generated using kanpai by verifying that the first commit
    contains the kanpai commit signature
    """

    # retrieving first commit of current working directory
    # git log --oneline returns one commit per line
    # 2>/dev/null eliminates errors but not the standard output,
    # which is read by os.popen
    # tail -1 retrieves the first commit of the git repo
    git_log_cmd = "git log --oneline 2>/dev/null " \
                  " | tail -1"

    git_first_commit = os.popen(git_log_cmd).read()

    # checking whether first commit was performed by kanpai
    # TODO: import from canai script or common file
    commit_signature = "kanpai 🎉 🍰"  # uniquelly identifies a kanpai project

    if commit_signature not in git_first_commit:
        if print_error_if_not_within:
            print(Fore.RED + "This command needs to be run "
                  "within a kanpai generated project... 😅"
                  + Style.RESET_ALL)

        return False

    return True


def get_generated_project_top_level():
    """
    retrieves the top level of the generated kanpai project
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
