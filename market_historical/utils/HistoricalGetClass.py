import pandas as pd

from market_historical.utils.tools import csv_data_cln


class HistoricalGetClass():
    def __init__(self, root_fp="./data"):
        self.root_fp = root_fp
        self.raw_fp = f"{root_fp}/raw"
        self.cln_fp = f"{root_fp}/clean"
        pass

    def get_usa_unemployment(self):

        file_name = "usa_UNRATE"
        key_name = "unemployment"
        file_fp = f"{self.raw_fp}/{file_name}.csv"
        data_pd = csv_data_cln(file_fp=file_fp, date_col="DATE", rename_key_col={"UNRATE": key_name})
        data_pd.to_parquet(f"{self.cln_fp}/{file_name}.parquet", use_dictionary=False)

    def get_usa_fund_rate(self):
        file_name = "usa_Federal Funds Effective Rate_DFF"
        key_name = "fed_fund_rate"
        file_fp = f"{self.raw_fp}/{file_name}.csv"
        data_pd = csv_data_cln(file_fp=file_fp, date_col="DATE", rename_key_col={"DFF": key_name})
        data_pd.to_parquet(f"{self.cln_fp}/{file_name}.parquet", use_dictionary=False)

    def get_usa_core_inflation(self):
        file_name = "usa_core_inflation_SeriesReport-20230328012130_d21b5b"
        file_fp = f"{self.raw_fp}/{file_name}.xlsx"
        raw_data_pd = pd.read_excel(file_fp, skiprows=11)
        cln_data_pd = raw_data_pd.drop(["HALF1","HALF2"], axis=1)
        # Reshape the DataFrame from wide to long format
        cln_data_pd = pd.melt(cln_data_pd, id_vars=['Year'], var_name='month', value_name='value')

        # Combine 'year' and 'month' columns into a datetime column
        cln_data_pd['c_datetime'] = pd.to_datetime(cln_data_pd['Year'].astype(str) + '-' + cln_data_pd['month'].astype(str) + '-01', format='%Y-%b-%d')
        cln_data_pd = cln_data_pd.rename(columns={"value": "core_inflation"})
        cln_data_pd = cln_data_pd.sort_values("c_datetime")
        cln_data_pd[["c_datetime", "core_inflation"]].to_parquet(f"{self.cln_fp}/{file_name}.parquet", use_dictionary=False)
        print("bye")

    def get_usa_nyse(self):
        file_name = "usa_^NYA"
        # key_name = "unemployment"
        keep_cols = ["Open","High","Low","Close","Adj Close","Volume"]
        file_fp = f"{self.raw_fp}/{file_name}.csv"
        data_pd = csv_data_cln(file_fp=file_fp, date_col="Date", prefix={"nyse": keep_cols})
        data_pd.to_parquet(f"{self.cln_fp}/{file_name}.parquet", use_dictionary=False)

    def get_usa_nasdaq(self):
        file_name = "usa_^IXIC"
        # key_name = "unemployment"
        keep_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
        file_fp = f"{self.raw_fp}/{file_name}.csv"
        data_pd = csv_data_cln(file_fp=file_fp, date_col="Date", prefix={"nasdaq": keep_cols})
        data_pd.to_parquet(f"{self.cln_fp}/{file_name}.parquet", use_dictionary=False)