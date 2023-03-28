import datetime
import re

import requests
import pandas as pd
import lxml
import bs4


def hello(url):
    for url in urls:
        html = requests.get(url).content
        soup = bs4.BeautifulSoup(html, features="lxml")
        title = [_i.text.strip() for _i in list(soup.findAll('h1')) if 'historical' in _i.text.strip().lower()][0]
        titles_3 = [_i.text.strip() for _i in list(soup.findAll('h3')) if _i.text.strip().lower() != '']
        df_list = pd.read_html(html)
        df_list = [_df for _df in df_list if 'Date from' in _df.columns]
        if (len(titles_3) != len(df_list)) and len(titles_3) != 0:
            print('got an issue with headers and df list size')
            continue

        title = re.sub('\s', '', title)
        if len(titles_3) == 0:
            df_list[0].to_parquet(f'./data/{title}.parquet', use_dictionary=False)
        else:
            for _idx, _i in enumerate(titles_3):
                df = df_list[_idx]
                title_3 = re.sub('[%><]', '_', _i)
                title_3 = re.sub('\s', '', title_3)
                df.to_parquet(f'./data/{title}_{title_3}.parquet', use_dictionary=False)

    print('bye')


def clean_current():
    curr_files = [
        'OwnerOccupierhomeloaninterestrates.parquet',
        'Investmenthomeloaninterestrates.parquet'
    ]

    for _file in curr_files:
        data_raw = pd.read_parquet(f'./data/raw/{_file}')

        col_data = [
            'Principal & Interest rate',
            'Principal & Interest Package rate**',
            'Interest Only rate',
            'Interest Only Package rate**',
        ]
        remap_none = {'n/a': None, '':None}
        for _col in col_data:
            data_raw[[f'clean_{_col}_real', f'clean_{_col}_comparison']] = data_raw[_col].str.split('p.a', n=1, expand=True)
            two_vals = ['real','comparison']

            for _val in two_vals:

                col_name = f'clean_{_col}_{_val}'
                print(col_name)
                data_raw[col_name] = data_raw[col_name].str.replace('\xa0', '', regex=False)
                data_raw[col_name] = data_raw[col_name].str.strip('.')
                data_raw[col_name] = data_raw[col_name].str.replace('p.a. Comparison rate', '', regex=False)
                data_raw[col_name] = data_raw[col_name].str.strip()

                data_raw = data_raw.replace({col_name: remap_none})
                data_raw[col_name] = data_raw[col_name].str.rstrip('%').astype('float')
        data_raw.to_parquet(f'./data/raw/{"".join(_file.split(".")[:-1])}_clean.parquet', use_dictionary=False)
        # 0 = {str} 'createTimeStamp'
        # 1 = {str} 'Loan type'
        # 2 = {str} 'Principal & Interest rate'
        # 3 = {str} 'Principal & Interest Package rate**'
        # 4 = {str} 'Interest Only rate'
        # 5 = {str} 'Interest Only Package rate**'

        # 00 = {str} 'Extra Home Loan\n (Loan to Value ratio of 70% or less)*'
        # 01 = {str} 'Extra Home Loan\n (Loan to Value ratio of 70.01% to 80%)*'
        # 02 = {str} 'Extra Home Loan\n (Loan to Value ratio of 80.01% or more)*'
        # 03 = {str} 'Standard Variable Rate (SVR)'
        # 04 = {str} '1 Year Fixed Rate'
        # 05 = {str} '2 Year Fixed Rate'
        # 06 = {str} '3 Year Fixed Rate'
        # 07 = {str} '4 Year Fixed Rate'
        # 08 = {str} '5 Year Fixed Rate'
        # 09 = {str} 'Viridian Line of Credit'
        # 10 = {str} 'CommBank Green Loan'

    #     loan_types = data_raw['Loan type'].unique()
    #     for _loan in loan_types:
    #         data_loan = data_raw[data_raw['Loan type'] == _loan]

    print('bye')

    pass


def scrape_current():
    url = 'https://www.commbank.com.au/home-loans/interest-rates.html'
    html = requests.get(url).content
    soup = bs4.BeautifulSoup(html, features="lxml")
    data_table = soup.findAll('div', {'class': 'complex-table row-wrapper'})
    results = []
    for _i in data_table:
        title = _i.find('div', {'class': 'heading-section'}).text.strip().replace(' ', '')
        data_path = f'./data/raw/{title}.parquet'
        data_final = pd.read_parquet(data_path)
        headers = _i.find('div', {'class': 'complex-table-row header'}).findAll('div', {'class': 'complex-cell'})
        col_names = []
        for _i2 in headers:
            col_names.append(_i2.text.strip())
        data = _i.findAll('div', {'class': 'complex-table-row data'})
        for _i3 in data:
            data_row = _i3.findAll('div', {'class': 'complex-cell'})
            row_dict = {'createTimeStamp': datetime.datetime.now()}
            for _idx, _i4 in enumerate(data_row):
                val = _i4.text
                key = col_names[_idx]
                row_dict[key] = val.strip()
            results.append(row_dict)
        data_pd = pd.DataFrame(results)
        data_final = pd.concat([data_pd, data_final], ignore_index=True)
        data_final.to_parquet(f'./data/raw/{title}.parquet', use_dictionary=False)

        #
    print('bye')


if __name__ == '__main__':
    urls = [
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-no-fee-2015.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-no-fee.aspx',
        # important
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-svr-2015.aspx',
        # important
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-svr.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-1-year-gteed-2015.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-1-year-gteed.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/histor12discounted2015.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-12-month-discounted.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-rate-saver-2015.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-rate-saver.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/his-3-yr2015.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-3-year-rate-saver.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/fixed-rate.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-fixed-rate.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-line-of-credit.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-eqfs.aspx',
        'https://www.commbroker.com.au/Net/Documentum/interest-rates-fees/historical-interest-rates/historical-extra-home.aspx',
    ]
    # hello(urls)
    scrape_current()
    clean_current()
