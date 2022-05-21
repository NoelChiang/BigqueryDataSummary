import math
from datetime import datetime, timedelta
import pytz
import json
from MyModule.CommentTool import Comment
import traceback
from itertools import chain

# -- Import my bigquery package
from MyModule import BigQueryTool

# -- Import setting file for global parameters
import setting

# -- Import graph library and set
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd

sns.set()

# Set font to support chinese
mpl.rcParams["font.family"] = "WenQuanYi Zen Hei"
# in case minus sign is shown as box
mpl.rcParams["axes.unicode_minus"] = False


# Error log decorator
def error_message_output(func):
    def wrap(*args, **kwargs):
        try:
            return_value = func(*args, **kwargs)
            if return_value is not None:
                return return_value
        except:
            with open("error.log", "w") as log:
                traceback.print_exc(file=log)

    return wrap


@error_message_output
def makeDateInterval(start: datetime = None, end: datetime = None):
    # Return tuples with query start date and finish date
    # Format : YYYYMMdd
    # Meet bigquery daily dataset naming (ex. events_20200606)
    # If end is None, use yesterday as end since today's data is not ready in biguery
    endTime = end if end is not None else datetime.now() - timedelta(days=1)
    endYear = str(endTime.year)
    endMonth = (
        "0" + str(endTime.month) if len(str(endTime.month)) < 2 else str(endTime.month)
    )
    endDay = "0" + str(endTime.day) if len(str(endTime.day)) < 2 else str(endTime.day)
    endDate = endYear + endMonth + endDay
    startTime = start if start is not None else endTime - timedelta(days=30)
    startYear = str(startTime.year)
    startMonth = (
        "0" + str(startTime.month)
        if len(str(startTime.month)) < 2
        else str(startTime.month)
    )
    startDay = (
        "0" + str(startTime.day) if len(str(startTime.day)) < 2 else str(startTime.day)
    )
    startDate = startYear + startMonth + startDay
    return (startDate, endDate)


@error_message_output
def makeGraphTitleDateString(start: str, end: str):
    # Return string to present date interval
    # Format: YYYY/MM/dd~YYYY/MM/dd
    # Input format: YYYYMMdd
    return (
        start[:4]
        + "/"
        + start[4:6]
        + "/"
        + start[6:]
        + "~"
        + end[:4]
        + "/"
        + end[4:6]
        + "/"
        + end[6:]
    )


@error_message_output
def setupAxesLabelFont(ax, x: dict = None, y: dict = None):
    if x is not None:
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(x["fontsize"])
            tick.label.set_fontweight(x["fontweight"])
    if y is not None:
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(y["fontsize"])
            tick.label.set_fontweight(y["fontweight"])


@error_message_output
def reset_date_string_x_ticks_label(ax):
    sunday_index = []
    short_date_str_list = []
    for i in range(len(ax.xaxis.get_major_ticks())):
        tick = ax.xaxis.get_major_ticks()[i]
        date_str = tick.label.get_text()
        if len(date_str) != 8:
            continue
        date = datetime.strptime(date_str, "%Y%m%d")
        if date.weekday() == 6:
            sunday_index.append(i)
        short_date_str_list.append(date_str[-4:-2] + "/" + date_str[-2:])
    ax.set_xticklabels(labels=short_date_str_list)
    for i in range(len(ax.xaxis.get_major_ticks())):
        if i in sunday_index:
            ax.xaxis.get_major_ticks()[i].label.set_color("red")

@error_message_output
def drawEventChart(start: datetime = None, end: datetime = None):
    dateInterval = makeDateInterval(start=start, end=end)
    queryStr = """
        BigQuery SQL Query String
    """.format(
        dateInterval[0], dateInterval[1]
    )
    queryData = BigQueryTool.SqlCommander().send(queryStr)
    dataFrame = queryData.to_dataframe()
    # Summarize data and make suitable chart
    # ...
    # ...


