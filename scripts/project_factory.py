
from colorama import Fore, Style

import os
import re

from .project_context import COMMIT_SIGNATURE


class ProjectFactory():
    """
    handles the creation of a project from a template
    """

    def __init__(self, package_name, package_path, template_path,
                 replacements=None,
                 package_slug=None,
                 template_remote_url=None,
                 template_commit_hash=None):

        self.package_name = package_name
        self.package_path = package_path
        self.template_path = template_path

        self.replacements = replacements
        self.package_slug = package_slug

        self.template_remote_url = template_remote_url
        self.template_commit_hash = template_commit_hash

    def generate(self):
        """
        creates new project from template
        """

        # make sure package name is valid
        self.__assess_package_name()

        # make sure that we are not in a git repo
        self.__ensure_cwd_not_within_git_repo()

        # checking whether project already exists
        self.__ensure_project_does_not_exist()

        # retrieving package content
        self.__ensure_project_does_not_conflict()

        # create project from template
        self.__create_project_from_template()

        # init git repo
        self.__init_git_repo()

        # replace tokens in all files
        self.__replace_package_tokens()

        # replace package slug
        self.__replace_package_slug()

        # init git repo
        self.__commit_git_repo()

        print(Fore.GREEN + "\nProject %s successfully created! 🎉 🍰"
              % self.package_name)

    def __assess_package_name(self):
        is_valid = bool(re.match(r"^[a-zA-Z]\w*", self.package_name))

        if not is_valid:
            print(Fore.RED + "Invalid package name 😵"
                  + Style.RESET_ALL)
            print("Please use letters, numbers or underscores 🙏")

            exit(1)

    def __ensure_cwd_not_within_git_repo(self):
        """
        ensures cwd is not within a git repo
        """

        git_cmd = "git status &>/dev/null"

        git_code = os.system(git_cmd)

        if git_code == 0:
            cwd = os.getcwd()

            print(Fore.RED + "This appears to be a git repository 😵"
                  + Style.RESET_ALL)
            print("This command is going to create a git repository "
                  "of its own and cannot be run in a git repository")
            print("Current working directory is %s " % cwd)
            print("Please change working directory "
                  "before running this command 🙏")

            exit(1)

    def __ensure_project_does_not_exist(self):
        """
        ensures file with package name does not exist in cwd
        """

        if os.path.isfile(self.package_name) or os.path.isdir(self.package_name):
            print(Fore.RED + "Target location %s already exists 😨"
                  % self.package_name
                  + Style.RESET_ALL)
            print("Please use another project name 🙏")

            exit(1)

    def __ensure_project_does_not_conflict(self):
        """
        ensures project name does not exist within template package root
        """

        # list content of project template
        ls_template_cmd = "ls %s" % self.template_path

        template_content = os.popen(ls_template_cmd).read().split()

        if len(template_content) == 0:
            print(Fore.RED + "Error listing template package content: %s (%s) "
                  "😬"
                  % (template_content, ls_template_cmd)
                  + Style.RESET_ALL)

            exit(1)

        # checking whether projet name conflicts with package content
        for file in template_content:
            if file == self.package_name:
                print(Fore.RED + "Cannot create a project named %s 🙃"
                      % self.package_name
                      + Style.RESET_ALL)
                print("This project name conflicts with a ressource "
                      "inside of the template package")
                print("Please avoid the following project names 🙏")
                print(template_content)

                exit(1)

    def __create_project_from_template(self):
        """
        creates project from template
        """

        copy_cmd = "cp -R %s %s" % (self.template_path, self.package_name)

        copy_code = os.system(copy_cmd)

        if copy_code != 0:
            print(Fore.RED + "Error creating project: %s (%s) 😭"
                  % (copy_code, copy_cmd)
                  + Style.RESET_ALL)

            exit(1)

    def __init_git_repo(self):
        """
        creates git repo and adds commit containing commit signature
        """

        source_template = ""

        if self.template_remote_url is not None:

            source_template = "from %s (%s) " \
                % (self.template_remote_url, self.template_commit_hash)

        git_init_cmd = "cd %s " \
                       " && git init &>/dev/null " \
                       " && git add . " \
                       " && git commit -m 'initial commit %sby %s' &>/dev/null" \
                       % (self.package_name, source_template, COMMIT_SIGNATURE)

        git_init_code = os.system(git_init_cmd)

        if git_init_code != 0:
            print(Fore.RED + "Error initializing git repo: %s 🥺"
                  % git_init_code
                  + Style.RESET_ALL)

            exit(1)

    def __get_package_class(self, package_name):
        return ''.join([s.capitalize() for s in package_name.split("_")])

    def __replace_package_tokens(self):
        """
        replace template tokens within project
        """

        package_class = self.__get_package_class(self.package_name)

        escaped_package_path = re.escape(self.package_path).replace("/", "\\/")

        if self.replacements is None:

            # use default replacements
            replacements = dict(
                KAMPAI_PACKAGE_NAME=self.package_name,
                KAMPAI_PACKAGE_CLASS=package_class,
                KAMPAI_PACKAGE_ROOT=escaped_package_path,
                KAMPAI_PACKAGE_DESCRIPTION='Package description',
                KAMPAI_PACKAGE_SCRIPT='package_script_name')

        else:

            # use provided replacements
            replacements = self.replacements

        for key, value in replacements.items():

            # find . -type f recursively finds all files (only files)
            # grep -v git ignores files matching the pattern git
            # xargs converts the list of files into parameters for sed
            # sed -i '' 's/a/b/g' replaces the pattern a by b in the files
            replace_cmd = "cd %s " \
                          " && find . -type f " \
                          " | grep -v git " \
                          " | xargs sed -i '' 's/%s/%s/g' " \
                          % (self.package_name, key, value)

            replace_code = os.system(replace_cmd)

            if replace_code != 0:
                print(Fore.RED + "Error replacing tokens: %s (%s) 😳"
                      % (replace_code, replace_cmd)
                      + Style.RESET_ALL)

                exit(1)

    def __replace_package_slug(self):
        """
        renames template package folder according to project name
        """

        if self.package_slug is None:

            # use default directory name
            dir_replacements = dict(
                KAMPAI_PACKAGE_SLUG=self.package_name)
        else:

            # use provided directory name
            dir_replacements = {
                self.package_slug: self.package_name}

        for key, value in dir_replacements.items():

            dir_replace_cmd = "cd %s " \
                              " && mv %s %s" % (self.package_name, key, value)

            dir_replace_code = os.system(dir_replace_cmd)

            if dir_replace_code != 0:
                print(Fore.RED + "Error replacing dir tokens: %s (%s) 😢"
                      % (dir_replace_code, dir_replace_cmd)
                      + Style.RESET_ALL)

                exit(1)

    def __commit_git_repo(self):
        """
        commits token and slug changes
        """

        git_init_cmd = "cd %s " \
                       " && git add . " \
                       " && git commit -m 'replaced tokens' &>/dev/null " \
                       % self.package_name

        git_init_code = os.system(git_init_cmd)

        if git_init_code != 0:
            print(Fore.RED + "Error initializing git repo: %s 😞"
                  % git_init_code
                  + Style.RESET_ALL)

            exit(1)
