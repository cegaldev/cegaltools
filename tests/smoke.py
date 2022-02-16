# Copyright Cegal AS 2022
# For license terms, see LICENSE


import pandas as pd

from cegaltools.wells import Well


def test_well_from_las():
    Well(filename="15_9-F-14.las", path=r"examples/")


def test_well_from_dataframe():
    train = pd.read_csv(r"examples/train-small.csv", sep=";")
    filename = train.loc[train.WELL == "15/9-13"][train.columns[1:]]
    Well(filename=filename, dataframe_name="15/9-13", from_dataframe=True)
