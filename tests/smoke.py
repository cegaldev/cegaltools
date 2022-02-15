import pandas as pd

from cegaltools.wells import Well


def test_well_construction():
    Well(filename='15_9-F-14.las', path=r'examples/')

def test_train():
    train = pd.read_csv(r'examples/train-small.csv', sep=';')
    # print("JLG")
    # print("type(train) == ", type(train))

    # print(train)
    # print(train.columns[1:])

    filename = train.loc[train.WELL == '15/9-13'][train.columns[1:]]
    test_csv_well = Well(filename=filename,
                         dataframe_name='15/9-13',
                         from_dataframe=True)
