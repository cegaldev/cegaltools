__author__ = 'hilde haland'

import pandas as pd
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from cegaltools.cegaltools.utilities import Cegalutils
from cegaltools.utilities import Cegalutils


class CegalWellPlotter:

    @staticmethod
    def _positions(rows, cols):
        '''
        :param rows: int number of rows
        :param cols: int number of columns
        :return: a grid index for the set row and column numbers
        '''

        positions = []
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                positions.append((i, j))
        return positions

    def plot_logs(df, logs=None, log_scale_logs=None, lithology_logs=None, lithology_proba_logs=None,
                  lithology_description=None,
                  show_fig=True):
        '''
        :param df: cegaltools log dataframe
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

        '''

        if logs is None:
            logs = [x for x in list(df.columns) if
                    x not in Cegalutils.assert_list(lithology_logs) and x not in Cegalutils.assert_list(
                        lithology_proba_logs) and x not in Cegalutils.assert_list(log_scale_logs)]
        else:
            logs = list(logs)

        all_logs = Cegalutils.assert_list(logs) + Cegalutils.assert_list(log_scale_logs) + Cegalutils.assert_list(
            lithology_logs) + Cegalutils.assert_list(lithology_proba_logs)
        fig = make_subplots(rows=1,
                            cols=sum([len(logs), len(Cegalutils.assert_list(log_scale_logs)),
                                      len(Cegalutils.assert_list(lithology_logs)),
                                      len(Cegalutils.assert_list(lithology_proba_logs))]),
                            subplot_titles=all_logs,
                            y_title=df.index.name,
                            shared_yaxes=True)
        values = list(range(len(px.colors.qualitative.Vivid)))

        colorscale_count = 1

        for log in list(zip(all_logs, range(1, len(Cegalutils.assert_list(logs))
                                               + len(Cegalutils.assert_list(log_scale_logs))
                                               + len(Cegalutils.assert_list(lithology_proba_logs))
                                               + len(Cegalutils.assert_list(lithology_logs)) + 1))):

            if log[0] in Cegalutils.assert_list(logs):
                fig.append_trace(
                    go.Scatter(x=df[log[0]],
                               y=df[log[0]].index,
                               name=log[0],
                               hovertemplate=
                               '<b>Depth:</b>: %{y:.2f}' +
                               '<br><b>Log value</b>: %{x:.3f}<br>'),
                    row=1, col=log[1])

            elif log[0] in Cegalutils.assert_list(log_scale_logs):
                fig.append_trace(
                    go.Scatter(x=df[log[0]],
                               y=df[log[0]].index,
                               name=log[0],
                               hovertemplate=
                               '<b>Depth:</b>: %{y:.2f}' +
                               '<br><b>Log value</b>: %{x:.3f}<br>'),
                    row=1, col=log[1])
                fig.update_xaxes(type="log", row=1, col=log[1])

            elif log[0] in Cegalutils.assert_list(lithology_logs):
                fig.append_trace(
                    go.Heatmap(
                        z=df[log[0]].apply(lambda x: np.ones(3) * x),
                        y=df.index,
                        x=[0, 0.25, 0.5, 0.75, 1],
                        name=log[0],
                        colorscale=[x[1] for x in
                                    lithology_description.dictionary.values()] if lithology_description is not None
                        else px.colors.qualitative.Vivid[
                             :len([x for x in df[log[0]].unique() if ~np.isnan(x)])] if len(
                            [x for x in df[log[0]].unique() if
                             ~np.isnan(x)]) < 11 else Cegalutils.create_lith_log_colorscheme(df[log[0]]),
                        showscale=False,
                        hovertemplate=
                        '<b>Depth:</b>: %{y:.2f}' +
                        '<br><b>Cluster</b>: %{z}<br>', ),
                    row=1, col=log[1])

            elif log[0] in Cegalutils.assert_list(lithology_proba_logs):
                fig.append_trace(
                    go.Heatmap(
                        z=df[log[0]].apply(lambda x: np.ones(3) * x),
                        y=df.index,
                        x=[0, 0.25, 0.5, 0.75, 1],
                        name=log[0],
                        colorscale=Cegalutils.create_lith_PROBA_log_colorscheme('black'),
                        showscale=True if colorscale_count == 1 else False,
                        colorbar=dict(title=dict(text='FACIES PROBABILITY', side='right'), yanchor="middle"),
                        zmin=0,
                        zmax=1,
                        hovertemplate=
                        '<b>Depth:</b>: %{y:.2f}' +
                        '<br><b>Facies prob</b>: %{z:.3f}<br>'),
                    row=1, col=log[1])
                colorscale_count += 1

        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=800,
                          # width=len(logs) * 300,
                          margin=dict(t=200),
                          title={'text': '<br><b>Well log viewer</b>',
                                 'y': 0.9,
                                 'x': 0.0,
                                 'yanchor': 'top'},
                          showlegend=False)
        for annotation in [x for x in fig['layout']['annotations'] if df.index.name not in str(x)]:
            annotation['textangle'] = 0
            if len(all_logs) > 5:
                annotation['textangle'] = -45
            if (len(all_logs) > 9) or (len([x for x in all_logs if len(x) > 15]) > 0):
                annotation['textangle'] = -90
        #
        if show_fig:
            fig.show()
        else:
            return fig

    def plot_correlation(df, show_fig=True):
        '''

        :return: None

        Creates plotly correlation plot of all present cegaltools logs

        '''
        temp_df = df.corr().dropna(how='all', axis=0).dropna(how='all', axis=1)
        fig = px.imshow(temp_df,
                        labels=dict(x="Well log (horizontal)", y="Well log (vertical)", color="Correlation"),
                        x=temp_df.columns,
                        y=temp_df.columns)

        fig.update_xaxes(side='top')
        fig.update_layout(
            margin=dict(t=150, l=30, r=30, b=30),
            title={'text': '<b>Well log correlation matrix</b>',
                   'y': 0.9,
                   'x': 0.1,
                   'yanchor': 'top'},
        )
        if show_fig:
            fig.show()
        else:
            return fig

    def _plot_log_value_histograms(df, show_fig=True):
        '''

        :return: None
        '''
        cols = 4
        rows = math.ceil(len(df.columns) / cols)

        fig = make_subplots(rows=rows,
                            cols=cols,
                            subplot_titles=(df.columns))

        for histogram in (zip(CegalWellPlotter._positions(rows, cols), df.columns)):
            fig.append_trace(
                go.Histogram(
                    x=df[histogram[1]],
                    name=histogram[1],
                    hovertemplate=
                    '<b>Count</b>: %{y:.2f}' +
                    '<br><b>bin</b>: %{x}<br>'),
                histogram[0][0], histogram[0][1])

        fig.update_layout(height=rows * 200 + 420,
                          showlegend=False,
                          margin=dict(t=420),
                          title={
                              'text': '<br><br><b>Well log value histograms</b>' +
                                      '<br><br>Well log values for each log is plotted as a histogram to show '
                                      'distribution of values.' +
                                      '<br><br><i> - Use toolbar in top right corner to navigate the plot.',
                              'y': 0.9,
                              'yanchor': 'top'})
        if show_fig:
            fig.show()
        else:
            return fig

    def _plot_index_increment_histogram(df, show_fig=True):

        fig = go.Figure(go.Histogram(
            x=pd.Series(df.index).diff(),
            nbinsx=int(len(pd.Series(df.index)) / 100),
            name='',
            hovertemplate=
            '<b>Count</b>: %{y:.2f}' +
            '<br><b>Increment bin</b>: %{x}<br>'))

        fig.update_layout(height=750,
                          margin=dict(t=280),
                          xaxis_title_text='increment value',
                          title={
                              'text': '<b>Histogram of index increments</b>' +
                                      ' <br><br>With varying values for index increments the cegaltools logs' +
                                      '<br>should be further QCed or resampled before being used.' +
                                      '<br><br><i> - Use toolbar in top right corner to navigate the plot.',
                              'y': 0.9,
                              'yanchor': 'top'})

        if show_fig:
            fig.show()
        else:
            return fig

    def _plot_well_log_nulls(df, show_fig=True):

        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.index,
            xgap=1.1,
            name='',
            hovertemplate=
            '<b>Log</b>: %{x}' +
            '<br><b>Data</b>: %{z}' +
            '<br><b>Index</b>: %{y}<br>')
        )

        fig.update_layout(
            height=800,
            margin=dict(t=320),
            title={
                'text': '<br><br><b>Non-missing values for cegaltools logs</b>' +
                        ' <br><br>Present datapoints in cegaltools logs are visualized below,' +
                        '<br>missing coloration means the datapoint is NULL.' +
                        '<br><br><i> - Use toolbar in top right corner to navigate the plot.',
                'y': 0.9,
                'yanchor': 'top'})
        fig.update_xaxes(side='top')
        fig.update_yaxes(autorange="reversed", title='depth')
        fig.update_traces(dict(showscale=False,
                               coloraxis=None,
                               colorscale='gray'))

        if show_fig:
            fig.show()
        else:
            return fig

    def plot_coverage(df, show_fig=True):
        '''

        :param show_fig: returns plotly figure if set to False, shows figure if set to true (default True)
        :return:

        Plot shows the inverse fraction of missing data, i.e data coverage for individual logs
        '''

        coverage_df = pd.DataFrame(1 - df.isna().sum() / len(df)).reset_index().rename(
            columns={'index': 'log', 0: 'count'})

        fig = px.bar(coverage_df, x='log', y='count', color='count',
                     title='Relative data coverage of log values',
                     hover_data={'log': True, 'count': ':.2f'},
                     color_continuous_scale='blugrn')
        if show_fig:
            fig.show()
        else:
            return fig