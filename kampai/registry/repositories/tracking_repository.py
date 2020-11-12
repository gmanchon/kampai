
import mlflow
from mlflow.tracking import MlflowClient

from memoized_property import memoized_property

from collections.abc import Mapping

from colorama import Fore, Style


class TrackingRepository():

    def __init__(self, conf, experiment_name, code_commit_hash,
                 code_storage_location, model_storage_location):

        self.code_commit_hash = code_commit_hash
        self.experiment_name = experiment_name
        self.code_storage_location = code_storage_location
        self.model_storage_location = model_storage_location

        # get conf
        self.mlflow_uri = conf.server

        # check conf
        self.disabled = not self.__check_valid_conf()

        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled: "
                  + "invalid mlflow url %s 😭\n"
                  % self.mlflow_uri
                  + Style.RESET_ALL
                  + "Please configure the url of the mlflow server "
                  + "in the app.yaml conf file entry \"mlflow_uri\"")

        # remove trailing slash if any
        if self.mlflow_uri[-1] == "/":
            self.mlflow_uri = self.mlflow_uri[:-1]

        # create client
        mlflow.set_tracking_uri(self.mlflow_uri)
        self.mlflow_client = MlflowClient()

    def __check_valid_conf(self):
        """
        checks whether conf is correct
        """

        # check whether default value is used for mlflow uri
        return self.mlflow_uri != "https://url.of.the.mlflow.server/"

    @memoized_property
    def mlflow_experiment_id(self):
        """
        retrieves experiment if it already exists or creates it
        """

        # check conf
        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled..."
                  + Style.RESET_ALL)

            return

        try:
            # create experiment
            return self.mlflow_client.create_experiment(self.experiment_name)
        except BaseException:
            # retrieve existing experiment
            return self.mlflow_client.get_experiment_by_name(
                self.experiment_name).experiment_id

    def mlflow_create_run(self):
        """
        creates run for experiment and stores code commit hash,
        code storage location and model storage location in run tags
        """

        # check conf
        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled..."
                  + Style.RESET_ALL)

            return

        # run only once (TODO: use memoized property ?)
        if hasattr(self, 'mlflow_run'):
            return

        print(Fore.GREEN + "\nCreating tracking run..."
              + Style.RESET_ALL)

        self.mlflow_run = self.mlflow_client.create_run(
            self.mlflow_experiment_id)

        print(Fore.GREEN + "\nTracking created at:\n"
              + Style.RESET_ALL
              + f"{self.mlflow_uri}/#"
              + f"/experiments/{self.mlflow_experiment_id}"
              + f"/runs/{self.mlflow_run.info.run_id}")

        # set run tags
        self.mlflow_set_tags({
            "code storage": self.code_storage_location,
            "code commit hash": self.code_commit_hash,
            "model storage": self.model_storage_location})

    def mlflow_set_tag(self, key, value):
        """
        stores a tag in a run
        """

        # check conf
        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled..."
                  + Style.RESET_ALL)

            return

        # set tag
        self.mlflow_client.set_tag(
            self.mlflow_run.info.run_id, key, value)

    def mlflow_set_tags(self, items):
        """
        stores multiple tags in a run
        """

        # check conf
        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled..."
                  + Style.RESET_ALL)

            return

        # waiting for implementation of client set tags
        for key, value in items.items():
            self.mlflow_set_tag(key, value)

        # set tags
        # self.mlflow_client.set_tags(
        #     self.mlflow_run.info.run_id, items)

    def mlflow_log_param(self, key, value):
        """
        logs a param in a run
        """

        # check conf
        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled..."
                  + Style.RESET_ALL)

            return

        # create run
        self.mlflow_create_run()

        # log param
        self.mlflow_client.log_param(
            self.mlflow_run.info.run_id,
            key, value)

    def mlflow_log_metric(self, key, value):
        """
        stores a metric in a run
        """

        # check conf
        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled..."
                  + Style.RESET_ALL)

            return

        # create run
        self.mlflow_create_run()

        # log metric
        self.mlflow_client.log_metric(
            self.mlflow_run.info.run_id,
            key, value)

    def mlflow_log_dict_param(self, dict, radix):
        """
        stores nested parameters in a run
        """

        # check conf
        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled..."
                  + Style.RESET_ALL)

            return

        # create run
        self.mlflow_create_run()

        # iterate through dictionary
        key_radix = "%s__" % radix
        for key, value in dict.items():
            if isinstance(value, Mapping):
                # iterate recursively through sub dictionary
                self.mlflow_log_dict_param(value, key_radix + key)
            else:
                # other datatypes are converted to their string representation
                self.mlflow_log_param(key_radix + key, value)

    def mlflow_log_object_param(self, obj, radix):
        """
        stores nested objects and attributes in a run
        """

        # check conf
        if self.disabled:

            print(Fore.RED + "\n⚠️ Tracking repository disabled..."
                  + Style.RESET_ALL)

            return

        # create run
        self.mlflow_create_run()

        # iterate through object
        key_radix = "%s__" % radix
        for key, value in obj.__dict__.items():
            if hasattr(value, "__dict__"):
                # iterate recursively through sub object
                self.mlflow_log_object_param(value, key_radix + key)
            else:
                # other datatypes are converted to their string representation
                self.mlflow_log_param(key_radix + key, value)
