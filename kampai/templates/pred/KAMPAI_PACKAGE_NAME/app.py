
from KAMPAI_PACKAGE_NAME.trainer.trainer import Trainer

from colorama import Fore, Style


class App:

    def __init__(self):

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
