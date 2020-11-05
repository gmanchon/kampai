
import uuid

from colorama import Fore, Style

import re
import os


class ProjectClone():
    """
    handles the clone of a source template project
    """

    def __init__(self, source):

        # getting temporary directory name
        self.tmp_dir = self.__generate_tmp_directory_name()

        # cloning source
        self.__clone_repository(source, self.tmp_dir)

        # removing existing repo
        self.commit_hash, self.remote_url = \
            self._remove_cloned_directory_git_repo(self.tmp_dir)

    def is_valid(self):

        return True

    def get_clone_params(self):

        # return cloned directory params
        return (self.tmp_dir, self.commit_hash, self.remote_url)

    def remove_temporary_directory(self):

        # remove temporary directory
        self.__remove_temporary_directory(self.tmp_dir)

    def __generate_tmp_directory_name(self):
        """
        create unique directory name for git clone
        """

        # creating temporary directory
        tmp_dir = uuid.uuid4().hex

        while os.path.isfile(tmp_dir) or os.path.isdir(tmp_dir):

            print(Fore.RED + "Generated tmp location %s already exists 😨"
                  % tmp_dir
                  + Style.RESET_ALL
                  + "Generating a new one... 👽")

            # generate new temporary directory
            tmp_dir = uuid.uuid4().hex

        return tmp_dir

    def __clone_repository(self, source, tmp_dir):
        """
        clone repository to temporary directory
        """

        # cloning repository
        print(Fore.GREEN + "\nCloning repository... 🚀"
              + Style.RESET_ALL
              + "\nFrom: %s to %s" % (source, tmp_dir))

        # --progress allows to retrieve all of the output
        git_clone_cmd = f"git clone --progress {source} {tmp_dir} 2>&1"

        clone_res = os.popen(git_clone_cmd).read()

        # checking clone result
        is_match_1 = re.search(r"Receiving objects: .* done\.", clone_res)
        is_match_2 = re.search(r"Resolving deltas: .* done\.", clone_res)

        if not is_match_1 or not is_match_2:

            print(Fore.RED + "\n⚠️ Error cloning %s (%s) 😨"
                  % (source, git_clone_cmd)
                  + Style.RESET_ALL
                  + "\nMake sure %s is a valid git repository... 👽"
                  % source)

            # remove temporary directory if created
            self.__remove_temporary_directory(tmp_dir)

    def __remove_temporary_directory(self, dir_path):

        # remove directory
        remove_tmp_cmd = "rm -Rf %s" % dir_path

        os.system(remove_tmp_cmd)

    def _remove_cloned_directory_git_repo(self, tmp_dir):
        """
        remove .git directory in cloned directory
        in order to start from clean history
        """

        print(Fore.GREEN + "\nCleaning repository... 🧹"
              + Style.RESET_ALL)

        # retrieve latest commit hash
        git_latest_commit_hash_cmd = "cd %s " \
            % tmp_dir \
            + "&& git rev-parse master"

        commit_hash = os.popen(git_latest_commit_hash_cmd).read().strip()

        print("Clone hash: %s"
              % commit_hash)

        # list remotes
        git_remotes_cmd = "cd %s " \
            % tmp_dir \
            + "&& git config --get remote.origin.url"

        remote_url = os.popen(git_remotes_cmd).read().strip()

        print("Clone source: %s"
              % remote_url)

        # remove git directory
        remove_git_cmd = "cd %s " \
            % tmp_dir \
            + "&& rm -Rf .git"

        os.system(remove_git_cmd)

        return (commit_hash, remote_url)
