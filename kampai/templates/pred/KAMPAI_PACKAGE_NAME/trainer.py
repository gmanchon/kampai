
from KAMPAI_PACKAGE_NAME.data import get_data, clean_df
from KAMPAI_PACKAGE_NAME.pipeline import KAMPAI_PACKAGE_CLASSPipeline
from KAMPAI_PACKAGE_NAME.utils import compute_rmse

from sklearn.model_selection import train_test_split

import joblib


class Trainer():

    def train(self):

        # get data
        df = get_data()
        df = clean_df(df)

        # get X and y
        # TODO: not generic
        cols = ["pickup_latitude",
                "pickup_longitude",
                "dropoff_latitude",
                "dropoff_longitude"]

        y = df["fare_amount"]
        X = df[cols]

        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.1,
                                                            random_state=42)

        # create pipeline
        self.model = KAMPAI_PACKAGE_CLASSPipeline().create_pipeline()

        # train
        self.model.fit(X_train, y_train)

        # predict
        y_pred = self.model.predict(X_test)

        # perf
        rmse = compute_rmse(y_pred, y_test)

        # save model
        joblib.dump(self.model, 'model.joblib')

        return rmse


if __name__ == '__main__':

    # create trainer
    trainer = Trainer()

    print("Training model...")

    # running trainer
    rmse = trainer.train()

    from colorama import Fore, Style

    print(Fore.GREEN + "Model trained, rmse: %s 👍"
          % rmse
          + Style.RESET_ALL)
