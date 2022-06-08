import re

import requests
import pandas as pd
import lxml
import bs4

def hello(url):

    html = requests.get(url).content
    soup = bs4.BeautifulSoup(html, features="lxml")
    df_list = pd.read_html(html)
    df_list[0].to_parquet('./data/rba_cash_rate_target.parquet')

    print('bye')


if __name__ == '__main__':
    url = 'https://www.rba.gov.au/statistics/cash-rate/'

    hello(url)