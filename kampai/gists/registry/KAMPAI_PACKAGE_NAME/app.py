# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

from colorama import Fore, Style

from kampai.registry.registry import Registry

from KAMPAI_PACKAGE_NAME.conf.app_conf import load_conf
from KAMPAI_PACKAGE_NAME.trainer.trainer import Trainer


class App:

    def __init__(self):

        # load conf
        self.conf = load_conf()

        # load registry
        print(Fore.GREEN + "\nLoading registry..."
              + Style.RESET_ALL)

        self.registry = Registry(self.conf.registry)

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

        print(Fore.GREEN + "\nLog training in registry... 🚀"
              + Style.RESET_ALL)

        # log training
        self.registry.log_object_param(self.conf.trainer, "trainer")
        self.registry.log_metric("rmse", rmse)
        self.registry.log_model()

        print(Fore.GREEN + "\nTraining logged 👌"
              + Style.RESET_ALL)


def main():

    # create app
    app = App()

    # run app
    app.run()


if __name__ == '__main__':

    main()
