# pylint: disable=missing-docstring, invalid-name
# pylint: disable=too-few-public-methods, no-self-use

import joblib

from sklearn.model_selection import train_test_split

from KAMPAI_PACKAGE_NAME.trainer.data import get_data, clean_df
from KAMPAI_PACKAGE_NAME.trainer.pipeline import KAMPAI_PACKAGE_CLASSPipeline
from KAMPAI_PACKAGE_NAME.trainer.metrics import compute_rmse


class Trainer():

    def train(self):

        # get data
        df = get_data()
        df = clean_df(df)

        # get X and y
        cols = ["pickup_latitude",
                "pickup_longitude",
                "dropoff_latitude",
                "dropoff_longitude"]

        X = df[cols]
        y = df["fare_amount"]

        # holdout
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.1,
                                                            random_state=42)

        # create pipeline
        model = KAMPAI_PACKAGE_CLASSPipeline().create_pipeline()

        # train
        model.fit(X_train, y_train)

        # predict
        y_pred = model.predict(X_test)

        # perf
        rmse = compute_rmse(y_pred, y_test)

        # save model
        joblib.dump(model, 'model.joblib')

        return rmse
