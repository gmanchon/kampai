
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
        tmp_dir = self.__generate_tmp_directory_name()

        # cloning source
        self.__clone_repository(source, tmp_dir)

    def is_valid(self):

        return True

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
        print(Fore.GREEN + "\nCloning repository %s... 🚀"
              % source
              + Style.RESET_ALL)

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
            remove_tmp_cmd = "rm -Rf %s" % tmp_dir

            os.system(remove_tmp_cmd)
