import re

import mplcursors as mplcursors
import numpy as np
import requests
import pandas as pd
from pandas.api.types import is_numeric_dtype
import lxml
import bs4
from matplotlib import pyplot as plt
import plotly.express as px

from scipy.interpolate import interp1d, Rbf

def plot_data(data_input: pd.DataFrame, y_values: list):
    data_input_pd = data_input

    fig = px.line(data_input_pd,
                  x='Date from',
                  y=y_values,
                  title="layout.hovermode='x unified'",
                  # color='feat_prop_type'
                  )
    fig.update_traces(mode="markers+lines", hovertemplate=None, connectgaps=True)
    fig.update_layout(hovermode="x unified")

    fig.show()



# 00 = {str} 'Date from'
# 01 = {str} 'Cash rate target %'
# 02 = {str} 'Owner occupied (principal and interest)(%pa)'
# 03 = {str} 'ehl70_pi'
# 04 = {str} '1 Year Fixed (%pa)'
# 05 = {str} '2 Year Fixed (%pa)'
# 06 = {str} '3 Year Fixed (%pa)'
# 07 = {str} '4 Year Fixed (%pa)'
# 08 = {str} '5 Year Fixed (%pa)'
# 09 = {str} 'Percentage Change from Corresponding Quarter of Previous Year ;  All groups CPI ;  Australia ;'
# 10 = {str} 'Unemployment rate ;  Persons ;.1'
# 11 = {str} 'confidence'