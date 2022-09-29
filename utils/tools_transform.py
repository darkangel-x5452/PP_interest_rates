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


def get_combine_df(got_rba_rate, rates_list):
    got_rba_rate = got_rba_rate.rename(columns={'Effective Date': 'Date from'})
    date_col = 'Date from'
    combined_pd = rates_list[0]
    if len(rates_list) > 1:
        for _i in range(1, len(rates_list)):
            combined_pd = pd.concat([combined_pd, rates_list[_i]])
    combined_pd = pd.concat([got_rba_rate, combined_pd])
    combined_pd[date_col] = pd.to_datetime(combined_pd[date_col], errors='coerce')
    combined_pd = combined_pd.sort_values(date_col)
    combined_pd = combined_pd.dropna(subset=[date_col])
    result_pd = pd.DataFrame({})
    result_pd.loc[:, date_col] = combined_pd[[date_col]]
    for _idx, _i in enumerate(combined_pd.columns):
        if _i == date_col:
            continue
        col_dropna = combined_pd[_i].dropna()
        last_val = col_dropna.tolist()[-1]
        # last_row = combined_pd.iloc[-1, _idx]
        # if last_row:
        combined_pd.iloc[-1, _idx] = last_val
        if is_numeric_dtype(combined_pd[_i]):
            result_pd.loc[:, _i] = combined_pd.loc[:, _i]
        print('bye')
    result_pd = result_pd.sort_values(date_col)
    result_pd = result_pd.ffill()


    # NOTE: fillna between values: https://stackoverflow.com/questions/68883770/how-to-fill-nan-values-between-two-values
    result_pd.to_csv('./data/result.csv')
    result_pd.to_parquet('./data/result.parquet')
    return result_pd