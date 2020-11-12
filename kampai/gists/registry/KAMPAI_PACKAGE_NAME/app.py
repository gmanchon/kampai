# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

from colorama import Fore, Style

from KAMPAI_PACKAGE_NAME.conf.app_conf import load_conf
from KAMPAI_PACKAGE_NAME.trainer.trainer import Trainer


class App:

    def __init__(self):

        # load conf
        self.conf = load_conf()

        # create trainer
        self.trainer = Trainer()

    def run(self):

        print(Fore.GREEN + "\nTrain model..."
              + Style.RESET_ALL)

        # train model
        rmse = self.trainer.train()

        print(Fore.GREEN + "\nModel trained, RMSE: %s 👍"
              % rmse
              + Style.RESET_ALL)


def main():

    # create app
    app = App()

    # run app
    app.run()


if __name__ == '__main__':

    main()
