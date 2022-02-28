# Copyright Cegal AS 2022
# For license terms, see LICENSE

__author__ = "hildehaland"

import lasio
import os
import hashlib
import pandas as pd
import json
from cegal.welltools.utilities import Cegalutils
from cegal.welltools.plotting import CegalWellPlotter as cwp


class Well:

    """
    The purpose of this tool is to provide an easy go-to solution for plotting of cegal.welltools logs.
    The tool was built to accept .las files as cegal.wellstools inout but has been edited to accept a dataframe as input for use
    in the Force 2020 Machine Learning hackathon.

    The tool uses lasio to create cegal.welltools objects that can add curves and write file to disk, please refer to lasio
    documentation for more info (https://lasio.readthedocs.io/en/latest/).

    This package uses simpler syntax, but trades off customization options.

    To create a cegal.welltools object from a dataframe pass the dataframe object to the "filename" parameter, instead of a
    string, and leave path at None. Set "from_dataframe" to True. By passing a string to the "dataframe_name"
    parameter you can specify a cegal.welltools name added to the lasio object that will be created.

    Methods for cegal Well object:

     df() - returns cegal.welltools log data as a dataframe
     report() - returns a cegal.welltools report consisting of three plots providing an overview of the cegal.welltools data,
     refer to function for more information
     plot_logs() - uses the cegal.welltools plotter to return a log section of selected wells. It accepts line plot,
     lithology logs and lithology probability logs. You can also specify lithology colours using a lithology dictionary.
     plot_correlation() - returns a correlation plot of all logs with non-null values
     add_to_well() - allows you to add a derived cegal.welltools log to you Well object
     write_las() - writes a las file of the current object to disk

    """

    def __init__(
        self, filename=None, path=None, from_dataframe=False, dataframe_name=None
    ):
        """

        :param filename: input filename
        :param path: path to file
        :param from_dataframe: Booelan value indicating if input data is from a pandas dataframe
        :param dataframe_name: optional well name if pandas dataframe is source
        """
        ## Read data from las file at specifiec path location, throw error if filename is not a string
        if not from_dataframe:
            if type(filename) == pd.core.frame.DataFrame:
                raise ValueError(
                    'To create cegal.welltools from a pandas dataframe or numpy array set "from_dataframe" to True'
                )
            if type(filename) is str:
                try:
                    assert filename.lower().endswith(".las")
                except AssertionError:
                    raise (
                        AssertionError(
                            "Filename not valid, input must be a las-file with extension .las"
                        )
                    )
        else:
            try:
                assert type(filename) == pd.core.frame.DataFrame
                print(
                    "Well objects will assume the first dataframe column as depth curve, please assert that the "
                    "passed dataframe has the correct column order"
                )
            except ValueError:
                raise ValueError(
                    "Input data type is not accepted. Pass a pandas dataframe or set parameter "
                    '"from_dataframe" to False and pass a .las file to create a Well object'
                )

        self.path = path if path is not None else ""
        if not from_dataframe:
            self.filename = (
                filename if type(filename) is str and filename is not None else None
            )
        else:
            self.filename = (
                filename
                if type(filename) is pd.core.frame.DataFrame and filename is not None
                else None
            )
        self.well_object = (
            lasio.read(os.path.join(self.path, self.filename))
            if from_dataframe is False and filename.lower().endswith(".las")
            else Cegalutils._create_well_object(
                dataframe=self.filename, dataframe_name=dataframe_name
            )
        )
        self.id = hashlib.sha224(
            json.dumps(self.df().to_dict()).encode("utf-8")
        ).hexdigest()

    def df(self):
        """

        :return: pandas.DataFrame containing cegal.welltools logs from las file
        """
        return self.well_object.df()

    def report(self, show_fig=True):
        """

        :return: None
        Generates three plots from functions
         - self._plot_index_increment_histogram()
         - self._plot_well_log_nulls()
         - self._plot_log_value_histograms()
        """

        if show_fig:
            cwp._plot_index_increment_histogram(self.df(), show_fig=show_fig)
        else:
            fig1 = cwp._plot_index_increment_histogram(self.df(), show_fig=show_fig)

        if show_fig:
            cwp._plot_well_log_nulls(self.df(), show_fig=show_fig)
        else:
            fig2 = cwp._plot_well_log_nulls(self.df(), show_fig=show_fig)

        if show_fig:
            cwp._plot_log_value_histograms(self.df(), show_fig=show_fig)
        else:
            fig3 = cwp._plot_log_value_histograms(self.df(), show_fig=show_fig)

        if not show_fig:
            return [fig1, fig2, fig3]

    def plot_logs(
        self,
        logs=None,
        log_scale_logs=None,
        lithology_logs=None,
        lithology_proba_logs=None,
        lithology_description=None,
        show_fig=True,
    ):
        """


        :param logs: list of logs to plot as line plots
        :param log_scale_logs=None : list og logs to be plotted on a logartihmic scale
        :param lithology_logs: list of lithology logs to be plotted as heatmaps
        :param lithology_proba_logs: list of lithology probability logs to be plotted as black/grey heatmaps
        :param lithology_description: A dictionary containing name and color information for lithology logs
        :param show_fig: show (True) or return (False) figure
        :return: None

        A lihtology description is a dictionary with lithology log values as keys and a tuples containing lithology
        name and colour (Hex Code/html name):
                lithology_value_3: ('lst', '#bb4cd0'),

                example dict:
                    lithology_dict = {
                                        1.0: ('sand', '#e6e208'),
                                        2.0: ('shale', '#0b8102'),
                                        3.0: ('lst', 'Orange'),
                                    }

        """

        if show_fig:
            cwp.plot_logs(
                self.df(),
                logs,
                log_scale_logs,
                lithology_logs,
                lithology_proba_logs,
                lithology_description,
                show_fig=show_fig,
            )
        else:
            fig = cwp.plot_logs(
                self.df(),
                logs,
                log_scale_logs,
                lithology_logs,
                lithology_proba_logs,
                lithology_description,
                show_fig=show_fig,
            )
            return fig

    def plot_correlation(self, show_fig=True):
        """


        :return: None
        """

        if show_fig:
            cwp.plot_correlation(self.df(), show_fig=show_fig)
        else:
            fig = cwp.plot_correlation(self.df(), show_fig=show_fig)
            return fig

    def plot_coverage(self, show_fig=True):
        """

        :param show_fig:
        :return:
        """
        if show_fig:
            cwp.plot_coverage(self.df(), show_fig=show_fig)
        else:
            fig = cwp.plot_coverage(self.df(), show_fig=show_fig)
            return fig

    def add_to_well(
        self, log_series, log_name="lithology", descr="added lithology log", unit="unit"
    ):
        """
        ;param log_series: tuple containing self.id for the cegal.welltools and pandas series of values (cegaltools.id, pd.Series)
        :param log_name: string containing lithology log name (defaults to lithology)
        :param descr: log description (defaults to 'added lithology log')
        :return:


        """
        try:
            assert self.id == log_series[0]

            if isinstance(log_series[1], pd.Series):
                self.well_object.insert_curve(
                    ix=len(self.well_object.df().columns) + 1,
                    mnemonic=log_name,
                    data=log_series[1],
                    unit=unit,
                    descr=descr,
                )
            elif isinstance(log_series[1], pd.DataFrame):
                for col in [
                    x for x in log_series[1].columns if x not in self.df().columns
                ]:
                    self.well_object.insert_curve(
                        ix=len(self.well_object.df().columns) + 1,
                        mnemonic="{}_{}".format(col, log_name)
                        if "proba" in col
                        else "{}_description".format(log_name)
                        if "description" in col
                        else log_name,
                        data=log_series[1][col],
                        unit=unit,
                        descr=descr,
                    )
        except AssertionError:
            raise AssertionError(
                "Logs can only be added to the cegal.welltools.wells.Well object it was created from. "
                "Please attach new log_series to the appropriate cegal.welltools.wells.Well object."
            )

    def write_las(self, filename=None):
        """

        :param filename: User can add the output name of the file, this is required for a pandas input cegal.welltools
        :return:
        """
        if filename is None:
            filename = os.path.join(
                Cegalutils._replace_none(self.path),
                Cegalutils._create_unique_name_at_save_location(self),
            )
        else:
            filename = os.path.join(
                Cegalutils._replace_none(self.path), filename + ".las"
            )
        with open(filename, "w") as fp:
            pass
        self.well_object.write(filename)
