
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates

def drawdown_graph(series, ax=None):
    
    if ax is None:
        ax = plt.gca()

    if not isinstance(series,pd.Series):
        raise TypeError("input must be pandas series")

    # Do math
    log_returns = np.log(series/series.shift(1)).dropna()
    cumulative_returns = log_returns.cumsum()

    # Calculating drawdown
    drawdown = (cumulative_returns - cumulative_returns.cummax())
    deepest  = (cumulative_returns - cumulative_returns.cummax()).cummin()*100
    filt = deepest.min() == deepest
    deepest_date = deepest.loc[filt].index[0]

    uwater   = (cumulative_returns - (cumulative_returns).cummax()) < 0
    runs     = (~uwater).cumsum()[uwater]
    counts   = runs.value_counts(sort=True).iloc[:1]
    max_dur  = counts.iloc[0]

    inds     = runs == counts.index[0]
    inds     = (inds).where(inds)
    start    = inds.first_valid_index()
    end      = inds.last_valid_index()

    # Create plot
    ax.plot(drawdown * 100,color="red")

    # Y axis
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax.fill_between(drawdown.index,drawdown*100,0,alpha=0.5,color="red")

    ylim_decision = min(ax.get_ylim()[0]+1, ax.get_ylim()[0]*0.98)

    ax.fill_betweenx([0,ax.get_ylim()[0]],start,end,color="grey",zorder=0,alpha=0.5)
    ax.set_ylim(ylim_decision,0)

    # X axis

    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

    if len(log_returns) >= 252*4:
        # Long time period
        ax.xaxis.set_major_locator(mdates.YearLocator())
        # ax1.xaxis.set_minor_locator(mdates.MonthLocator())
    elif len(log_returns) >= 252*2:
        # Medium time period
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
    else:
        # Short time period
        ax.xaxis.set_major_locator(mdates.MonthLocator())

    # ax.autofmt_xdate()

    # Info

    drawdown_info = {"max drawdown %":f"{deepest.min():.2f}%", "max drawdown date": deepest_date, "duration start": start, "duration end": end,"days drawdown": f"{max_dur}"}
    # max_dur/len(data)*100:.2f
    
    return ax, drawdown_info