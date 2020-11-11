# pylint: disable=missing-docstring, invalid-name

import os

import pandas as pd


def get_data():

    # build data path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_path = os.path.join(project_root, "data", "data.csv")

    # read csv
    df = pd.read_csv(data_path)

    return df


def clean_df(df):

    df = df.dropna(how='any', axis='rows')

    # remove observations with invalid pickup or dropoff coordinates
    df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0)]
    df = df[(df.pickup_latitude != 0) | (df.pickup_longitude != 0)]

    df = df[df["pickup_latitude"].between(left=40, right=42)]
    df = df[df["pickup_longitude"].between(left=-74.3, right=-72.9)]
    df = df[df["dropoff_latitude"].between(left=40, right=42)]
    df = df[df["dropoff_longitude"].between(left=-74, right=-72.9)]

    # remove observations with invalid fare amount
    if "fare_amount" in list(df):
        df = df[df.fare_amount.between(0, 4000)]

    # remove observations with invalid passenger count
    df = df[df.passenger_count < 8]
    df = df[df.passenger_count >= 0]

    return df
