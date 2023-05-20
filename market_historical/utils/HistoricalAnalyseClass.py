import datetime

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px

class HistoricalAnalyseClass():
    def __init__(self, root_fp="./data"):
        self.root_fp = root_fp
        self.raw_fp = f"{root_fp}/raw"
        self.cln_fp = f"{root_fp}/clean"

    def combine_data(self):
        usa_files = [
            "usa_^IXIC.parquet",
            "usa_^NYA.parquet",
            "usa_core_inflation_SeriesReport-20230328012130_d21b5b.parquet",
            "usa_Federal Funds Effective Rate_DFF.parquet",
            "usa_UNRATE.parquet",
            "usa_cpi_non-season_CPIAUCNS.parquet"
        ]
        number_cols = [
            'nasdaq_Open',
            'nasdaq_High',
            'nasdaq_Low',
            'nasdaq_Close',
            'nasdaq_Adj Close',
            'nasdaq_Volume',
            'nyse_Open',
            'nyse_High',
            'nyse_Low',
            'nyse_Close',
            'nyse_Adj Close',
            'nyse_Volume',
            'core_inflation',
            'fed_fund_rate',
            'unemployment',
            'cpi_CPIAUCNS',
            'cpi_CPIAUCNS_former'
        ]
        combined_pd = pd.DataFrame({"c_datetime": {}})
        for _file in usa_files:
            data_pd = pd.read_parquet(f"{self.cln_fp}/{_file}")
            combined_pd = pd.merge(combined_pd, data_pd, on='c_datetime', how="outer")
        combined_pd = combined_pd.sort_values("c_datetime")
        # combined_pd = combined_pd[(combined_pd['c_datetime'] > '2012-01-01') & (combined_pd['c_datetime'] < '2019-01-01')]
        today = datetime.datetime.now()
        # today = '2023-04-30'
        combined_pd.loc[combined_pd['c_datetime'] <= today, :] = combined_pd.loc[combined_pd['c_datetime'] <= today, :].fillna(method='ffill')

        scaler = MinMaxScaler(feature_range=(0, 1))  # Create a scaler object with a range of 0 to 1
        combined_pd[number_cols] = scaler.fit_transform(combined_pd[number_cols])  # Scale the 'col1' and 'col2' columns

        combined_pd.to_parquet(f"{self.cln_fp}/combined_data.parquet", use_dictionary=False)
        print("bye")

    def analyse_data(self):
        data_pd = pd.read_parquet(f"{self.cln_fp}/combined_data.parquet")
        data_pd = data_pd[(data_pd['c_datetime'] > '2012-01-01') & (data_pd['c_datetime'] < '2019-01-01')]
        number_cols = [
            # 'nasdaq_Open',
            # 'nasdaq_High',
            # 'nasdaq_Low',
            # 'nasdaq_Close',
            # 'nasdaq_Adj Close',
            # 'nasdaq_Volume',
            # 'nyse_Open',
            # 'nyse_High',
            # 'nyse_Low',
            'nyse_Close',
            # 'nyse_Adj Close',
            # 'nyse_Volume',
            'core_inflation',
            'fed_fund_rate',
            'unemployment',
            'cpi_CPIAUCNS',
            'cpi_CPIAUCNS_former'
        ]
        fig = px.line(data_pd,
                      x='c_datetime',
                      y=number_cols,
                      title="layout.hovermode='x unified'",
                      # color='feat_prop_type'
                      )
        fig.update_traces(mode="markers+lines", hovertemplate=None, connectgaps=True)
        fig.update_layout(hovermode="x unified")

        fig.show()
