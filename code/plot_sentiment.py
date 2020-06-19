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
    # create a list of cities from the dataframe when no cities are passed
    if city_list == None:
        city_list = list(df_copy.city.unique())
    # pass to plotting function depending on parameter passed
    if plotting == 'top10':
        top10(df_copy, city_list, colors, sampling, save, kwargs)

    elif plotting == 'subplots':
        subplot(df_copy, city_list, colors, sampling, save, kwargs)

    elif plotting == 'plots':
        plot(df_copy, city_list, colors, sampling, save, kwargs)

# function to print top10 vs bottom10 from dataframe tagged with 1,0
def top10(df_copy, city_list, colors, sampling, save, kwargs):
    plt.figure(figsize=kwargs.get('figsize', (16, 9))) # plot the figure onto which the lines will be traced
    df_plot_1 = df_copy[df_copy.top_10 == 1].resample(
        sampling, on='date').mean() # plot first trace after resampling
    plt.plot(df_plot_1.dropna().index,  # X axis
             df_plot_1['text_polarity'].dropna(),  # Y axis
             label='Most strict',  #set label
             color='Red',  # set color
             linewidth=kwargs.get('linewidth', 1), # pull parameter from kwargs dict
             )
    df_plot_2 = df_copy[df_copy.top_10 != 1].resample(
        sampling, on='date').mean()
    plt.plot(df_plot_2.dropna().index,  # X axis
             df_plot_2['text_polarity'].dropna(),  # Y axis
             label='Least strict',
             color='blue',
             linewidth=kwargs.get('linewidth', 1) # pull parameter from kwargs dict
             )
    plt.xticks(ticks=df_plot_1.index, labels=df_plot_1.index.strftime(
        '%-m-%d'), rotation=70, fontsize=kwargs.get('tick_font_size', 10))
    plt.yticks(fontsize=kwargs.get('tick_font_size', 10)). # pull parameters from kwargs dict
    legend = plt.legend(fontsize=kwargs.get('legend_font_size', None))
    if kwargs.get('remove_legend'):  # if kwarg is passed, remove legend from plot
        legend.remove()
    plt.title(kwargs.get('title', None),  
              fontsize=kwargs.get('title_font_size', 30)) # pull parameters from kwargs dict
    plt.xlabel(xlabel=kwargs.get('xlabel', None),
               fontsize=kwargs.get('label_font_size', 20))  # pull parameters from kwargs dict
    plt.ylabel(ylabel=kwargs.get('ylabel', None),
               fontsize=kwargs.get('label_font_size', 20))  # pull parameters from kwargs dict
    plt.xlim(df_plot_1.dropna().index.min(), df_plot_1.dropna().index.max())  # pull set xlimits to limits of x data
    if kwargs.get('ylim'):  # pull parameters from kwargs dict, this needs an if statement bc any parameter will disable autoscaling
        plt.ylim(kwargs.get('ylim', None))  # pull parameters from kwargs dict
    plt.tight_layout()  # use tightlayout
    if kwargs.get('save_legend', False):  # pass to export_legend function if kwarg 'save_legend' is passed
        try:
            export_legend(legend=legend, filename=save+"_legend")
        except ValueError:  # raise error if there is no save path passed
            raise
    if save != None:  # if a filepath is passed, save the figure at the path
        try:
            plt.savefig(save)
            print(f'Figure successfully saved at {save}!')  # print success
        except ValueError:
            raise  # raise error if filepath is unusable

# function to print subplots
def subplot(df_copy, city_list, colors, sampling, save, kwargs):
    fig, axes = plt.subplots(len(city_list), figsize=kwargs.get(
        'figsize', (16, (2*len(city_list)))), sharey=kwargs.get('sharey', 'none'))  # create the canvas onto which the lines will be traced
    # create a plot on different ax for each city
    for ax, city, color in zip(axes.flatten(), sorted(city_list), cycle(colors)): # flatten axes to make iterable and zip with city_list and colors
        df_plot = df_copy[df_copy.city == city].resample(
            sampling, on='date').mean()  # resample dataframe
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

# function to print all cities on one plot with unique colors
# code is similar to the previous functions
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

# function to print legend 
def export_legend(legend, filename, expand=[-5, -5, 5, 5]):
    fig = legend.figure  # grab legend from figure
    fig.canvas.draw()  # redraw legend canvas
    bbox = legend.get_window_extent()  # create boundary box (bbox) by getting the extents of legend figure
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))  # unpack add 5 pixel padding to bbox extents
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())  # takes the figure dpi and transforms it into display coords
    fig.savefig(filename, dpi="figure", bbox_inches=bbox) # saves figure at filepath
