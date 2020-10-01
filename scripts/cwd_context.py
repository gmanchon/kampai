
from colorama import Fore, Style

import os


def ensure_cwd_not_within_git_repo():
    """
    ensures cwd is not within a git repo
    """

    git_cmd = "git status &>/dev/null"

    git_code = os.system(git_cmd)

    if git_code == 0:
        cwd = os.getcwd()

        print(Fore.RED + "This appears to be a git repository 😵"
              + Style.RESET_ALL)
        print("This command is going to create a git repository of its own "
              "and cannot be run in a git repository")
        print("Current working directory is %s " % cwd)
        print("Please change working directory before running this command 🙏")

        exit(1)


def ensure_project_does_not_exist(package_name):
    """
    ensures file with package name does not exist in cwd
    """

    if os.path.isfile(package_name) or os.path.isdir(package_name):
        print(Fore.RED + "Target location %s already exists 😨" % package_name
              + Style.RESET_ALL)
        print("Please use another project name 🙏")

        exit(1)


def ensure_project_does_not_conflict(package_name, template_path):
    """
    ensures project name does not exist within selected template package root
    """

    # list content of project template
    ls_template_cmd = "ls %s" % template_path

    template_content = os.popen(ls_template_cmd).read().split()

    if len(template_content) == 0:
        print(Fore.RED + "Error listing template package content: %s (%s) 😬"
              % (template_content, ls_template_cmd)
              + Style.RESET_ALL)

        exit(1)

    # checking whether projet name conflicts with package content
    for file in template_content:
        if file == package_name:
            print(Fore.RED + "Cannot create a project named %s 🙃"
                  % package_name
                  + Style.RESET_ALL)
            print("This project name conflicts with a ressource "
                  "inside of the template package")
            print("Please avoid the following project names 🙏")
            print(template_content)

            exit(1)


def create_project_from_template(package_name, template_path):
    """
    creates project from template
    """

    copy_cmd = "cp -R %s %s" % (template_path, package_name)

    copy_code = os.system(copy_cmd)

    if copy_code != 0:
        print(Fore.RED + "Error creating project: %s (%s) 😭"
              % (copy_code, copy_cmd)
              + Style.RESET_ALL)

        exit(1)


def init_git_repo(package_name):
    """
    creates git repo and adds commit containing commit signature
    """

    commit_signature = "kanpai 🎉 🍰"  # uniquelly identifies a kanpai project

    git_init_cmd = "cd %s " \
                   " && git init &>/dev/null " \
                   " && git add . " \
                   " && git commit -m 'initial commit by %s' &>/dev/null" \
                   % (package_name, commit_signature)

    git_init_code = os.system(git_init_cmd)

    if git_init_code != 0:
        print(Fore.RED + "Error initializing git repo: %s 🥺" % git_init_code
              + Style.RESET_ALL)

        exit(1)


def replace_package_tokens(package_name):
    """
    replace template tokens within project
    """

    replacements = dict(
        CANAI_PACKAGE_NAME=package_name,
        CANAI_PACKAGE_DESCRIPTION='Package description',
        CANAI_PACKAGE_SCRIPT='package_script_name')

    for key, value in replacements.items():

        # find . -type f recursively finds all files (only files)
        # grep -v git ignores files matching the pattern git
        # xargs converts the list of files into parameters for sed
        # sed -i '' 's/a/b/g' replaces the pattern a by b in the files
        replace_cmd = "cd %s " \
                      " && find . -type f " \
                      " | grep -v git " \
                      " | xargs sed -i '' 's/%s/%s/g' " \
                      % (package_name, key, value)

        replace_code = os.system(replace_cmd)

        if replace_code != 0:
            print(Fore.RED + "Error replacing tokens: %s (%s) 😳"
                  % (replace_code, replace_cmd)
                  + Style.RESET_ALL)

            exit(1)


def replace_package_slug(package_name):
    """
    renames template package folder according to project name
    """

    dir_replacements = dict(
        CANAI_PACKAGE_SLUG=package_name)

    for key, value in dir_replacements.items():

        dir_replace_cmd = "cd %s " \
                          " && mv %s %s" % (package_name, key, value)

        dir_replace_code = os.system(dir_replace_cmd)

        if dir_replace_code != 0:
            print(Fore.RED + "Error replacing dir tokens: %s (%s) 😢"
                  % (dir_replace_code, dir_replace_cmd)
                  + Style.RESET_ALL)

            exit(1)


def commit_git_repo(package_name):
    """
    commits token and slug changes
    """

    git_init_cmd = "cd %s " \
                   " && git add . " \
                   " && git commit -m 'replaced tokens' &>/dev/null " \
                   % package_name

    git_init_code = os.system(git_init_cmd)

    if git_init_code != 0:
        print(Fore.RED + "Error initializing git repo: %s 😞" % git_init_code
              + Style.RESET_ALL)

        exit(1)


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
