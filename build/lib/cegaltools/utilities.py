__author__ = 'hilde haland'

import os
from colour import Color
from colour import rgb2hex
import plotly.express as px
import re
import datetime
import pandas
import lasio


class Cegalutils():

    def _create_unique_name_at_save_location(well, new_path=None):

        if well.filename is not None:
            suffix = 2
            new_name = ''.join([well.filename.split('.las')[0], '_v{}'.format(suffix)]) + '.las'
            while new_name in os.listdir(well.path):
                suffix += 1
                new_name = ''.join([well.filename.split('.las')[0],
                                    '_v{}'.format(suffix)]) + '.las'
        else:
            new_name = 'well_log_output_{}.las'.format(str(datetime.datetime.now().date()))
            if new_path is not None:
                joined = ''.join([new_path, new_name])
                new_name = joined
        return new_name

    def _replace_none(x):
        if x is None:
            return ''
        else:
            return x

    def assert_list(l):
        if l is None:
            return []
        elif isinstance(l, list) is not True:
            return [l]
        else:
            return l

    @staticmethod
    def _global_colorscheme():
        colorscheme = []
        for color in px.colors.qualitative.Vivid:
            rgb_string = re.findall(r'\d+', color)
            rgb_tuple = tuple(int(i) for i in rgb_string)
            colorscheme.append(rgb2hex(rgb_tuple)[:7])
        return colorscheme

    def create_lith_log_colorscheme(lith_log):
        colorscheme = Cegalutils._global_colorscheme()
        local_colorscheme = []
        for i in range(9):
            local_colorscheme.extend([x.hex for x in list(
                Color(colorscheme[i]).range_to(Color(colorscheme[i + 1]), (len(lith_log.unique()) // 10) + 1))][:-1])
        for i in range(9, 10):
            local_colorscheme.extend([x.hex for x in list(Color(colorscheme[i]).range_to(Color(colorscheme[i + 1]), len(
                lith_log.unique()) // 10 + len(lith_log.unique()) % 10))])
        return local_colorscheme

    def create_lith_PROBA_log_colorscheme(color):
        return [x.hex for x in list(Color('lightgrey').range_to(Color(color), 50))]

    def assert_input(input, type, error):
        """
        :param input: variable
        :param type: variable type
        :param error: error message
        :return: TypeError
        """
        try:
            assert isinstance(input, type)
        except TypeError:
            raise TypeError(error)

    def return_string_dict(lithology_dictionary, reverse=False):
        temp_dict = {}
        for key in lithology_dictionary.dictionary.keys():
            for val in [x[0] for x in lithology_dictionary.dictionary.values()]:
                if val == str(lithology_dictionary.dictionary[key][0]):
                    temp_dict.update({key: val})
        if reverse:
            return dict(zip(temp_dict.values(), temp_dict.keys()))
        else:
            return temp_dict

    def _create_well_object(dataframe, dataframe_name=None):

        isinstance(dataframe, pandas.core.frame.DataFrame)

        las = lasio.LASFile()
        las.well.DATE = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        if dataframe_name:
            las.well.WELL = dataframe_name
        for curve in dataframe.columns:
            las.add_curve(curve, dataframe[curve], unit='')

        return las

