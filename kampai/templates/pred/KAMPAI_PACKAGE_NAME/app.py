
from KAMPAI_PACKAGE_NAME.trainer.trainer import Trainer

from colorama import Fore, Style


class App:

    def __init__(self):
        self.trainer = Trainer()

    def run(self):

        print(Fore.GREEN + "\nTraining model..."
              + Style.RESET_ALL)

        # training model
        rmse = self.trainer.train()

        print(Fore.GREEN + "\nModel trained, rmse: %s 👍"
              % rmse
              + Style.RESET_ALL)
