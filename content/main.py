from content.wells import Well
from content.plotting import CegalWellPlotter as cwp
import pandas as pd

#from cegaltools.content.tools import Well


def main():

    #content = Well(filename='15_9-F-14.LAS', path=r'C:\Users\hilde\Dev\Cegal Lab')

    #content.report()
    #content.plot_correlation()

    train = pd.read_csv(r'C:\Users\hilde\Dev\force 2020 hackathon\train.csv', sep=';')

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


if __name__ == "__main__":
    main()
