import argparse
import os
import sys

from cegaltools.wells import Well
from cegaltools.plotting import CegalWellPlotter as cwp
import pandas as pd

#from cegaltools.cegaltools.tools import Well


def main():
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    path = r''
    filename = r''
    file_path = r''

    if args.path:
        path = args.path

    if args.filename:
        # filename = path + os.sep + args.filename
        filename = args.filename

    if path:
        file_path = path + os.sep + filename
    else:
        file_path = filename

    if not os.path.isfile(file_path):
        parser.print_help(sys.stderr)
        parser.exit(1)

    if filename.lower().endswith('.las'):
        plot_las_well(filename=filename, path=path)
    elif filename.lower().endswith('.csv') and os.path.isfile(filename):
        plot_csv_well(file_path)
    else:
        parser.print_help(sys.stderr)
        parser.exit(1)

def plot_las_well(filename, path):
    # cegaltools = Well(filename='15_9-F-14.LAS', path=r'C:\Users\hilde\Dev\Cegal Lab')
    cegaltools = Well(filename=filename, path=path)

    cegaltools.report()
    cegaltools.plot_correlation()

def plot_csv_well(filename):
    # filename = r'C:\Users\hilde\Dev\force 2020 hackathon\train.csv'
    train = pd.read_csv(filename, sep=';')

    test_csv_well = Well(filename=train.loc[train.WELL == '15/9-13'][train.columns[1:]],
                         dataframe_name='15/9-13',
                         from_dataframe=True)

    #test_csv_well.report()

    #test_csv_well.plot_correlation()

    print(test_csv_well.df().head())
    #test_csv_well.write_las(filename='test_csv_well')


    '''    cwp.plot_logs(df=test_csv_well.df(),
                  logs=['GROUP', 'FORMATION', 'RMED', 'RDEP', 'RHOB', 'GR', 'NPHI', 'DTC', 'DTS'],
                  lithology_logs='FORCE_2020_LITHOFACIES_LITHOLOGY',
                  lithology_proba_logs='FORCE_2020_LITHOFACIES_CONFIDENCE')'''

    test_csv_well.plot_logs(logs=['GROUP','FORMATION','RMED', 'RDEP', 'RHOB', 'GR', 'NPHI', 'DTC', 'DTS'],
                            lithology_logs='FORCE_2020_LITHOFACIES_LITHOLOGY',
                            lithology_proba_logs='FORCE_2020_LITHOFACIES_CONFIDENCE')

    cwp.plot_logs(df=test_csv_well.df(),
                  logs=test_csv_well.df().columns[1:-2],
                  lithology_logs='FORCE_2020_LITHOFACIES_LITHOLOGY',
                  lithology_proba_logs='FORCE_2020_LITHOFACIES_CONFIDENCE')

def get_parser():
    parser = argparse.ArgumentParser('python cegaltools/main.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--filename',
        help="Filename for either a Las file or a Csv file to plot",
        required=False,
    )
    parser.add_argument(
        '--path',
        help="Directory path",
        required=False,
    )
    return parser


if __name__ == "__main__":
    main()
