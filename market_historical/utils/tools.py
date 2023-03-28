import pandas as pd


def csv_data_cln(file_fp="", date_col="", rename_key_col= dict({}), keep_cols=None, prefix=dict({})) -> pd.DataFrame():
    if keep_cols is None:
        keep_cols = []
    data_pd = pd.read_csv(file_fp)
    rename_cols = []
    keep_cols = keep_cols
    prefix_cols = []
    if date_col != "":
        data_pd["c_datetime"] = pd.to_datetime(data_pd[date_col], errors='coerce')
    if len(rename_key_col) != 0:
        data_pd = data_pd.rename(columns=rename_key_col)
        rename_cols = list(rename_key_col.values())
    if len(prefix) != 0:
        for _k, _v in prefix.items():
            prefix_jn = {_item: f"{_k}_{_item}" for _item in _v}
            data_pd = data_pd.rename(columns=prefix_jn)
            prefix_cols = list(prefix_jn.values())



    data_pd =data_pd.sort_values("c_datetime")
    return data_pd[["c_datetime"]+rename_cols+keep_cols+prefix_cols]
