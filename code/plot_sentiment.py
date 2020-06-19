# import cycle to help make city,color tuples
from itertools import cycle
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_sentiment(df, city_list=None, plotting='plots', sampling='D', color=None, save=None, **kwargs):
    '''
    Parameters
    ----------
    df : Pandas DataFrame
        Name of the dataframe you wish to plot
    city_list : list, optional
        List of cities in DataFrame to plot. Default is None and will plot all cities.
    plotting : str, optional
        Options = 'plots', 'subplots', 'top10'. Default is 'plots'.
            'plots' returns plot of all cities in city_list on one plot.
            'subplots' returns a plot for each city in city_list.
            'top10' returns cities grouped by if they were in the top10 stictest or not.
    sampling : str, optional
        Offset aliases to pass to the .resample() method. Default is 'D'.
    color : list, optional
        Specify a ist of colors to plot cities in. Format for a city_list of ['city1', 'city2'] is ['color1', 'color2'].
    save : str, optional
        Filepath where you want the image saved to, Default is None.
    **kwargs : keyword arguments passed to matplotlib. Not all kwargs are available.

    '''

    # check for color parameterpull colors list from matplotlib
    if color != None:
        colors = color
    else:
        # if no color param, then pull colors list from matplotlib
        prop_cycle = plt.rcParams['axes.prop_cycle']
        colors = prop_cycle.by_key()['color']
    # make a copy of df so changes don't apply to original
    df_copy = df.copy()
    # make date column into datetime again
    df_copy.date = pd.to_datetime(df_copy.date + " " + df_copy.time)

    if city_list == None:
        city_list = list(df_copy.city.unique())

    if plotting == 'top10':
        top10(df_copy, city_list, colors, sampling, save, kwargs)

    elif plotting == 'subplots':
        subplot(df_copy, city_list, colors, sampling, save, kwargs)

    elif plotting == 'plots':
        plot(df_copy, city_list, colors, sampling, save, kwargs)


def top10(df_copy, city_list, colors, sampling, save, kwargs):
    plt.figure(figsize=kwargs.get('figsize', (16, 9)))
    df_plot_1 = df_copy[df_copy.top_10 == 1].resample(
        sampling, on='date').mean()
    plt.plot(df_plot_1.dropna().index,  # X axis
             df_plot_1['text_polarity'].dropna(),  # Y axis
             label='Most strict',
             color='Red',
             linewidth=kwargs.get('linewidth', 1),
             )
    df_plot_2 = df_copy[df_copy.top_10 != 1].resample(
        sampling, on='date').mean()
    plt.plot(df_plot_2.dropna().index,  # X axis
             df_plot_2['text_polarity'].dropna(),  # Y axis
             label='Least strict',
             color='blue',
             linewidth=kwargs.get('linewidth', 1)
             )
    plt.xticks(ticks=df_plot_1.index, labels=df_plot_1.index.strftime(
        '%-m-%d'), rotation=70, fontsize=kwargs.get('tick_font_size', 10))
    plt.yticks(fontsize=kwargs.get('tick_font_size', 10))
    legend = plt.legend(fontsize=kwargs.get('legend_font_size', None))
    if kwargs.get('remove_legend'):
        legend.remove()
    plt.title(kwargs.get('title', None),
              fontsize=kwargs.get('title_font_size', 30))
    plt.xlabel(xlabel=kwargs.get('xlabel', None),
               fontsize=kwargs.get('label_font_size', 20))
    plt.ylabel(ylabel=kwargs.get('ylabel', None),
               fontsize=kwargs.get('label_font_size', 20))
    plt.xlim(df_plot_1.dropna().index.min(), df_plot_1.dropna().index.max())
    if kwargs.get('ylim'):
        plt.ylim(kwargs.get('ylim', None))
    plt.tight_layout()
    if kwargs.get('save_legend', False):
        try:
            export_legend(legend=legend, filename=save+"_legend")
        except ValueError:
            raise
    if save != None:
        try:
            plt.savefig(save)
            print(f'Figure successfully saved at {save}!')
        except ValueError:
            raise


def subplot(df_copy, city_list, colors, sampling, save, kwargs):
    fig, axes = plt.subplots(len(city_list), figsize=kwargs.get(
        'figsize', (16, (2*len(city_list)))), sharey=kwargs.get('sharey', 'none'))
    for ax, city, color in zip(axes.flatten(), sorted(city_list), cycle(colors)):
        df_plot = df_copy[df_copy.city == city].resample(
            sampling, on='date').mean()
        ax.plot(df_plot.dropna().index,  # X axis
                df_plot['text_polarity'].dropna(),  # Y axis
                label=city,
                color=color,
                linewidth=kwargs.get('linewidth', 1)
                )
        ax.set(xticks=(df_plot.index),
               xticklabels=(df_plot.index.strftime('%-m-%d')),
               ylim=(kwargs.get('ylim', None)),
               xlabel=(kwargs.get('xlabel', None)),
               ylabel=(kwargs.get('ylabel', None)),
               title=(f'{city}'),
               )
    fig.suptitle(kwargs.get('suptitle', None), fontsize=30)
    if kwargs.get('suptitle', None):
        plt.tight_layout(rect=(0, 0, 1, .96))
    else:
        plt.tight_layout()
    if save != None:
        try:
            plt.savefig(save)
            print(f'Figure successfully saved at {save}!')
        except ValueError:
            raise


def plot(df_copy, city_list, colors, sampling, save, kwargs):
    plt.figure(figsize=kwargs.get('figsize', (16, 9)))
    for city, color in zip(sorted(city_list), cycle(colors)):
        df_plot = df_copy[df_copy.city == city].resample(
            sampling, on='date').mean()
        plt.plot(df_plot.dropna().index,  # X axis
                 df_plot['text_polarity'].dropna(),  # Y axis
                 label=city,
                 color=color,
                 linewidth=kwargs.get('linewidth', 1)
                 )
        plt.xticks(ticks=df_plot.index, labels=df_plot.index.strftime(
            '%-m-%d'), rotation=70, fontsize=kwargs.get('tick_font_size', 10))
        plt.yticks(fontsize=kwargs.get('tick_font_size', 10))
        legend = plt.legend(ncol=kwargs.get('legend_ncol', 3),
                            fontsize=kwargs.get('legend_font_size', None))
        if kwargs.get('remove_legend'):
            legend.remove()
        plt.title(kwargs.get('title', None),
                  fontsize=kwargs.get('title_font_size', 30))
        plt.xlabel(xlabel=kwargs.get('xlabel', None),
                   fontsize=kwargs.get('label_font_size', 20))
        plt.ylabel(ylabel=kwargs.get('ylabel', None),
                   fontsize=kwargs.get('label_font_size', 20))
        plt.xlim(df_plot.dropna().index.min(), df_plot.dropna().index.max())
        if kwargs.get('ylim'):
            plt.ylim(kwargs.get('ylim', None))
        plt.tight_layout()
    if kwargs.get('save_legend', False):
        try:
            export_legend(legend=legend, filename=save+"_legend")
        except ValueError:
            raise
    if save != None:
        try:
            plt.savefig(save)
            print(f'Figure successfully saved at {save}!')
        except ValueError:
            raise


def export_legend(legend, filename, expand=[-5, -5, 5, 5]):
    fig = legend.figure
    fig.canvas.draw()
    bbox = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)
