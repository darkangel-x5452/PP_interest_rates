import re

import mplcursors as mplcursors
import numpy as np
import requests
import pandas as pd
from pandas.api.types import is_numeric_dtype
import lxml
import bs4
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d, Rbf


def got_cba_svr():
    # 1 = {str} 'Existing loans (%pa)'
    # 2 = {str} 'New loans (%pa)'
    cba_svr_old = pd.read_parquet('data/raw/StandardVariableRateHistoricalRates(2008-2014).parquet')

    # 1 = {str} 'Owner occupied (principal and interest)(%pa)'
    # 2 = {str} 'Owner occupied (interest only)(%pa)'
    # 3 = {str} 'Investment (principal and interest)(%pa)'
    # 4 = {str} 'Investment (interest only)(%pa)'
    cba_svr_new = pd.read_parquet('data/raw/StandardVariableRateHistoricalRates-2015onwards.parquet')
    cba_svr_old = cba_svr_old.rename(columns={'Existing loans (%pa)': 'Owner occupied (principal and interest)(%pa)'})
    cba_svr_curr = pd.read_parquet('data/raw/OwnerOccupierhomeloaninterestrates_clean.parquet')
    # 06 = {str} 'clean_Principal & Interest rate_real'
    # 07 = {str} 'clean_Principal & Interest rate_comparison'
    # 08 = {str} 'clean_Principal & Interest Package rate**_real'
    # 09 = {str} 'clean_Principal & Interest Package rate**_comparison'
    # 10 = {str} 'clean_Interest Only rate_real'
    # 11 = {str} 'clean_Interest Only rate_comparison'
    # 12 = {str} 'clean_Interest Only Package rate**_real'
    # 13 = {str} 'clean_Interest Only Package rate**_comparison'

    # 1 = {str} 'Owner occupied (principal and interest)(%pa)'
    # 2 = {str} 'Owner occupied (interest only)(%pa)'
    # 3 = {str} 'Investment (principal and interest)(%pa)'
    # 4 = {str} 'Investment (interest only)(%pa)'
    rename_cols = {
        'createTimeStamp': 'Date from',
        'clean_Principal & Interest rate_real': 'Owner occupied (principal and interest)(%pa)',
        # 'clean_Interest Only rate_real': 'Owner occupied (interest only)(%pa)',
    }
    cba_svr_curr = cba_svr_curr[cba_svr_curr['Loan type'] == 'Standard Variable Rate (SVR)']
    cba_svr_curr = cba_svr_curr.rename(columns=rename_cols)
    cba_svr_curr = cba_svr_curr[list(rename_cols.values())]

    combined_pd = pd.concat([cba_svr_old[['Date from', 'Owner occupied (principal and interest)(%pa)']], cba_svr_new[['Date from', 'Owner occupied (principal and interest)(%pa)']]])
    combined_pd = pd.concat([combined_pd, cba_svr_curr])
    combined_pd['Date from'] = pd.to_datetime(combined_pd['Date from'], dayfirst=True)
    combined_pd = combined_pd.sort_values('Date from')
    print('bye')
    return combined_pd


def get_rba_rate():
    rba_rate = pd.read_parquet('data/raw/rba_cash_rate_target.parquet')
    rba_rate['Effective Date'] = pd.to_datetime(rba_rate['Effective Date'], format='%d %b %Y', errors='coerce')
    rba_rate['Cash rate target %'] = pd.to_numeric(rba_rate['Cash rate target %'], errors='coerce')
    rba_rate = rba_rate.dropna(subset=['Cash rate target %', 'Effective Date'])
    print('bye')
    return rba_rate
    pass


class Cursor:
    """
    A cross hair cursor.
    """

    def __init__(self, ax):
        self.ax = ax
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        # text location in axes coordinates
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
        if not event.inaxes:
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            # update the line positions
            self.horizontal_line.set_ydata(y)
            self.vertical_line.set_xdata(x)
            self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))
            self.ax.figure.canvas.draw()


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
    result_pd.to_csv('./data/result.csv')
    result_pd.to_parquet('./data/result.parquet')
    result_pd = result_pd  # .set_index(date_col, drop=True)
    use_lines = True
    if use_lines:
        result_pd = result_pd.set_index(date_col, drop=True)
        lines = result_pd.interpolate(method='linear').plot.line()
    else:
        fig, ax = plt.subplots()
        ax.set_title('Simple cursor')
        x = result_pd[date_col]
        # print(result_pd.columns)
        data_cols = [
            'Cash rate target %',
            'Owner occupied (principal and interest)(%pa)',
            'ehl70_pi',
            '1 Year Fixed (%pa)',
            '2 Year Fixed (%pa)',
            '3 Year Fixed (%pa)',
            '4 Year Fixed (%pa)',
            '5 Year Fixed (%pa)'
        ]
        for _i in data_cols:
            y = result_pd[_i]
            ax.scatter(x, y)#,linestyle='solid')

        cursor = Cursor(ax)
        fig.canvas.mpl_connect('motion_notify_event', cursor.on_mouse_move)

    plt.show()

    print('bye')
    pass


def got_cba_ehl70():
    # 0 = {str} 'Date from'
    # 1 = {str} 'Owner occupied (principal and interest)(%pa)'
    # 2 = {str} 'Owner occupied (interest only)(%pa)'
    # 3 = {str} 'Investment (principal and interest)(%pa)'
    # 4 = {str} 'Investment (interest only)(%pa)'
    cba_svr_old = pd.read_parquet('data/raw/ExtraHomeLoanHistoricalRates(2015onwards)_ExtraHomeLoan≤70_LVR.parquet')
    cba_svr_curr = pd.read_parquet('data/raw/OwnerOccupierhomeloaninterestrates_clean.parquet')
    # 06 = {str} 'clean_Principal & Interest rate_real'
    # 07 = {str} 'clean_Principal & Interest rate_comparison'
    # 08 = {str} 'clean_Principal & Interest Package rate**_real'
    # 09 = {str} 'clean_Principal & Interest Package rate**_comparison'
    # 10 = {str} 'clean_Interest Only rate_real'
    # 11 = {str} 'clean_Interest Only rate_comparison'
    # 12 = {str} 'clean_Interest Only Package rate**_real'
    # 13 = {str} 'clean_Interest Only Package rate**_comparison'

    # 1 = {str} 'Owner occupied (principal and interest)(%pa)'
    # 2 = {str} 'Owner occupied (interest only)(%pa)'
    # 3 = {str} 'Investment (principal and interest)(%pa)'
    # 4 = {str} 'Investment (interest only)(%pa)'
    rename_cols = {
        'createTimeStamp': 'Date from',
        'clean_Principal & Interest rate_real': 'Owner occupied (principal and interest)(%pa)',
        'clean_Interest Only rate_real': 'Owner occupied (interest only)(%pa)',
    }
    cba_svr_curr = cba_svr_curr[cba_svr_curr['Loan type'] == 'Extra Home Loan\n (Loan to Value ratio of 70% or less)*']
    cba_svr_curr = cba_svr_curr.rename(columns=rename_cols)
    cba_svr_curr = cba_svr_curr[list(rename_cols.values())]
    cba_svr_old['Date from'] = pd.to_datetime(cba_svr_old['Date from'], dayfirst=True)  # , errors='coerce')
    combined_pd = pd.concat([cba_svr_old, cba_svr_curr])
    combined_pd = combined_pd.sort_values('Date from')
    combined_pd = combined_pd.rename(columns={'Owner occupied (principal and interest)(%pa)': 'ehl70_pi'})
    print('bye')
    return combined_pd[['Date from', 'ehl70_pi']]


def got_cba_fr():
    # 0 = {str} 'Date from'
    # 1 = {str} '1 Year Fixed (%pa)'
    # 2 = {str} '2 Year Fixed (%pa)'
    # 3 = {str} '3 Year Fixed (%pa)'
    # 4 = {str} '4 Year Fixed (%pa)'
    # 5 = {str} '5 Year Fixed (%pa)'
    cba_svr_old = pd.read_parquet('data/raw/FixedRateHistoricalRates(2008-2014).parquet')
    cba_svr_old = cba_svr_old.rename(columns={'1 Year Fixed (%pa)': '1 Year Fixed (%pa)', '5 Year Fixed (%pa)': '5 Year Fixed (%pa)'})

    # 0 = {str} 'Date from'
    # 1 = {str} '1 Year Fixed (%pa)'
    # 2 = {str} '2 Year Fixed (%pa)'
    # 3 = {str} '3 Year Fixed (%pa)'
    # 4 = {str} '4 Year Fixed (%pa)'
    # 5 = {str} '5 Year Fixed (%pa)'
    cba_svr_new = pd.read_parquet('data/raw/FixedRateHistoricalRates-2015onwards_Owneroccupied-PrincipalandInterest.parquet')
    # cba_svr_old = cba_svr_old.rename(columns={'Existing loans (%pa)':'Owner occupied (principal and interest)(%pa)'})

    cba_svr_curr = pd.read_parquet('data/raw/OwnerOccupierhomeloaninterestrates_clean.parquet')
    replace_rows = {
        '1 Year Fixed Rate': '1 Year Fixed (%pa)',
        '2 Year Fixed Rate': '2 Year Fixed (%pa)',
        '3 Year Fixed Rate': '3 Year Fixed (%pa)',
        '4 Year Fixed Rate': '4 Year Fixed (%pa)',
        '5 Year Fixed Rate': '5 Year Fixed (%pa)',
    }
    rename_cols = {
        'createTimeStamp': 'Date from',
        'clean_Principal & Interest rate_real': 'Owner occupied (principal and interest)(%pa)',

    }
    cba_svr_curr = cba_svr_curr[cba_svr_curr['Loan type'].isin(replace_rows.keys())]
    cba_svr_curr = cba_svr_curr.replace({'Loan type': replace_rows})
    cba_svr_curr = cba_svr_curr.rename(columns=rename_cols)
    keep_cols = list(rename_cols.values())
    keep_cols.append('Loan type')
    cba_svr_curr = cba_svr_curr[keep_cols]
    cba_svr_curr = cba_svr_curr.reset_index().pivot(index='Date from', values='Owner occupied (principal and interest)(%pa)', columns='Loan type')
    combined_pd = pd.concat([cba_svr_old, cba_svr_new], ignore_index=True)
    combined_pd = pd.concat([combined_pd, cba_svr_curr], ignore_index=True)

    combined_pd['Date from'] = pd.to_datetime(combined_pd['Date from'], dayfirst=True)
    combined_pd = combined_pd.sort_values('Date from')
    print('bye')
    return combined_pd


def get_inflation():
    inflation_pd = pd.read_parquet('./data/refined/TABLES 1 and 2. CPI All Groups, Index Numbers and Percentage Changes_640101.parquet')
    return inflation_pd

def get_unemployment():
    unemployment_pd = pd.read_parquet('./data/refined/employment_data_6202001.parquet')
    return unemployment_pd

def get_confidence():
    unemployment_pd = pd.read_parquet('./data/refined/consumer_confidence.parquet')
    return unemployment_pd


if __name__ == '__main__':
    get_cba_svr = got_cba_svr()
    # ExtraHomeLoanHistoricalRates(2015onwards)_ExtraHomeLoan≤70_LVR
    get_cba_ehl70 = got_cba_ehl70()
    # FixedRateHistoricalRates(2008-2014).parquet
    get_cba_fr = got_cba_fr()
    got_rba_rate = get_rba_rate()
    got_inflation = get_inflation()
    got_confidence = get_confidence()
    got_unemployment = get_unemployment()
    get_combine_df(
        got_rba_rate,
        [
            get_cba_svr,
            # get_cba_ehl70,
            # get_cba_fr,
            got_inflation,
            got_unemployment,
            got_confidence
        ]
    )
