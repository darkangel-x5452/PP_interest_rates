import pandas as pd
from matplotlib import pyplot as plt
def hello():
    # Percentage Change from Corresponding Quarter of Previous Year ;  All groups CPI ;  Australia ;
    # Unnamed: 0
    col_interest ='confidence'
    date_col = 'Date from'
    filename = 'consumer_confidence'
    data_pd = pd.read_csv(f'../data/raw/indirect/{filename}.csv')
    master_pd = pd.DataFrame({})
    for _row in data_pd.iterrows():
        row_pd = pd.DataFrame(_row[1])
        row_pd[date_col] = row_pd.index
        row_pd = row_pd.rename(columns={ row_pd.columns[0]: 'confidence'})
        row_pd = row_pd.reset_index()
        year = row_pd.iloc[0,1]
        row_pd[date_col] = str(year) +'-'+row_pd[date_col] + '-'+'01'
        row_pd = row_pd.iloc[1:-1, :]
        row_pd = row_pd.drop(columns='index')
        master_pd = pd.concat([master_pd, row_pd],ignore_index=True)
    print('bye')
    # keep_cols = [
    #     'Unnamed: 0',
    #     col_interest
    #
    # ]
    # data_pd = data_pd[keep_cols]
    # data_pd = data_pd.iloc[9:, :]
    master_pd[col_interest] = master_pd[col_interest].str.strip('*')
    master_pd[col_interest] = master_pd[col_interest].str.strip('^')
    master_pd[col_interest] = master_pd[col_interest].astype(float)
    master_pd[col_interest] = master_pd[col_interest]/5
    master_pd[date_col] = pd.to_datetime(master_pd[date_col])

    master_pd.to_parquet(f'../data/refined/{filename}.parquet', use_dictionary=False)
    #
    # master_pd = master_pd.set_index(date_col, drop=True)
    # master_pd.plot()
    # plt.show()
    # print('bye')


if __name__ == '__main__':
    hello()


# 000 = {str} 'Unnamed: 0'
# 001 = {str} 'Employed total ;  Persons ;'
# 002 = {str} 'Employed total ;  Persons ;.1'
# 003 = {str} 'Employed total ;  Persons ;.2'
# 004 = {str} 'Employed total ;  > Males ;'
# 005 = {str} 'Employed total ;  > Males ;.1'
# 006 = {str} 'Employed total ;  > Males ;.2'
# 007 = {str} 'Employed total ;  > Females ;'
# 008 = {str} 'Employed total ;  > Females ;.1'
# 009 = {str} 'Employed total ;  > Females ;.2'
# 010 = {str} '> Employed full-time ;  Persons ;'
# 011 = {str} '> Employed full-time ;  Persons ;.1'
# 012 = {str} '> Employed full-time ;  Persons ;.2'
# 013 = {str} '> Employed full-time ;  > Males ;'
# 014 = {str} '> Employed full-time ;  > Males ;.1'
# 015 = {str} '> Employed full-time ;  > Males ;.2'
# 016 = {str} '> Employed full-time ;  > Females ;'
# 017 = {str} '> Employed full-time ;  > Females ;.1'
# 018 = {str} '> Employed full-time ;  > Females ;.2'
# 019 = {str} '> Employed part-time ;  Persons ;'
# 020 = {str} '> Employed part-time ;  Persons ;.1'
# 021 = {str} '> Employed part-time ;  Persons ;.2'
# 022 = {str} '> Employed part-time ;  > Males ;'
# 023 = {str} '> Employed part-time ;  > Males ;.1'
# 024 = {str} '> Employed part-time ;  > Males ;.2'
# 025 = {str} '> Employed part-time ;  > Females ;'
# 026 = {str} '> Employed part-time ;  > Females ;.1'
# 027 = {str} '> Employed part-time ;  > Females ;.2'
# 028 = {str} 'Employment to population ratio ;  Persons ;'
# 029 = {str} 'Employment to population ratio ;  Persons ;.1'
# 030 = {str} 'Employment to population ratio ;  Persons ;.2'
# 031 = {str} 'Employment to population ratio ;  > Males ;'
# 032 = {str} 'Employment to population ratio ;  > Males ;.1'
# 033 = {str} 'Employment to population ratio ;  > Males ;.2'
# 034 = {str} 'Employment to population ratio ;  > Females ;'
# 035 = {str} 'Employment to population ratio ;  > Females ;.1'
# 036 = {str} 'Employment to population ratio ;  > Females ;.2'
# 037 = {str} 'Unemployed total ;  Persons ;'
# 038 = {str} 'Unemployed total ;  Persons ;.1'
# 039 = {str} 'Unemployed total ;  Persons ;.2'
# 040 = {str} 'Unemployed total ;  > Males ;'
# 041 = {str} 'Unemployed total ;  > Males ;.1'
# 042 = {str} 'Unemployed total ;  > Males ;.2'
# 043 = {str} 'Unemployed total ;  > Females ;'
# 044 = {str} 'Unemployed total ;  > Females ;.1'
# 045 = {str} 'Unemployed total ;  > Females ;.2'
# 046 = {str} '> Unemployed looked for full-time work ;  Persons ;'
# 047 = {str} '> Unemployed looked for full-time work ;  Persons ;.1'
# 048 = {str} '> Unemployed looked for full-time work ;  Persons ;.2'
# 049 = {str} '> Unemployed looked for full-time work ;  > Males ;'
# 050 = {str} '> Unemployed looked for full-time work ;  > Males ;.1'
# 051 = {str} '> Unemployed looked for full-time work ;  > Males ;.2'
# 052 = {str} '> Unemployed looked for full-time work ;  > Females ;'
# 053 = {str} '> Unemployed looked for full-time work ;  > Females ;.1'
# 054 = {str} '> Unemployed looked for full-time work ;  > Females ;.2'
# 055 = {str} '> Unemployed looked for only part-time work ;  Persons ;'
# 056 = {str} '> Unemployed looked for only part-time work ;  Persons ;.1'
# 057 = {str} '> Unemployed looked for only part-time work ;  Persons ;.2'
# 058 = {str} '> Unemployed looked for only part-time work ;  > Males ;'
# 059 = {str} '> Unemployed looked for only part-time work ;  > Males ;.1'
# 060 = {str} '> Unemployed looked for only part-time work ;  > Males ;.2'
# 061 = {str} '> Unemployed looked for only part-time work ;  > Females ;'
# 062 = {str} '> Unemployed looked for only part-time work ;  > Females ;.1'
# 063 = {str} '> Unemployed looked for only part-time work ;  > Females ;.2'
# 064 = {str} 'Unemployment rate ;  Persons ;'
# 065 = {str} 'Unemployment rate ;  Persons ;.1'
# 066 = {str} 'Unemployment rate ;  Persons ;.2'
# 067 = {str} 'Unemployment rate ;  > Males ;'
# 068 = {str} 'Unemployment rate ;  > Males ;.1'
# 069 = {str} 'Unemployment rate ;  > Males ;.2'
# 070 = {str} 'Unemployment rate ;  > Females ;'
# 071 = {str} 'Unemployment rate ;  > Females ;.1'
# 072 = {str} 'Unemployment rate ;  > Females ;.2'
# 073 = {str} '> Unemployment rate looked for full-time work ;  Persons ;'
# 074 = {str} '> Unemployment rate looked for full-time work ;  Persons ;.1'
# 075 = {str} '> Unemployment rate looked for full-time work ;  Persons ;.2'
# 076 = {str} '> Unemployment rate looked for full-time work ;  > Males ;'
# 077 = {str} '> Unemployment rate looked for full-time work ;  > Males ;.1'
# 078 = {str} '> Unemployment rate looked for full-time work ;  > Males ;.2'
# 079 = {str} '> Unemployment rate looked for full-time work ;  > Females ;'
# 080 = {str} '> Unemployment rate looked for full-time work ;  > Females ;.1'
# 081 = {str} '> Unemployment rate looked for full-time work ;  > Females ;.2'
# 082 = {str} '> Unemployment rate looked for only part-time work ;  Persons ;'
# 083 = {str} '> Unemployment rate looked for only part-time work ;  Persons ;.1'
# 084 = {str} '> Unemployment rate looked for only part-time work ;  Persons ;.2'
# 085 = {str} '> Unemployment rate looked for only part-time work ;  > Males ;'
# 086 = {str} '> Unemployment rate looked for only part-time work ;  > Males ;.1'
# 087 = {str} '> Unemployment rate looked for only part-time work ;  > Males ;.2'
# 088 = {str} '> Unemployment rate looked for only part-time work ;  > Females ;'
# 089 = {str} '> Unemployment rate looked for only part-time work ;  > Females ;.1'
# 090 = {str} '> Unemployment rate looked for only part-time work ;  > Females ;.2'
# 091 = {str} 'Labour force total ;  Persons ;'
# 092 = {str} 'Labour force total ;  Persons ;.1'
# 093 = {str} 'Labour force total ;  Persons ;.2'
# 094 = {str} 'Labour force total ;  > Males ;'
# 095 = {str} 'Labour force total ;  > Males ;.1'
# 096 = {str} 'Labour force total ;  > Males ;.2'
# 097 = {str} 'Labour force total ;  > Females ;'
# 098 = {str} 'Labour force total ;  > Females ;.1'
# 099 = {str} 'Labour force total ;  > Females ;.2'
# 100 = {str} 'Participation rate ;  Persons ;'
# 101 = {str} 'Participation rate ;  Persons ;.1'
# 102 = {str} 'Participation rate ;  Persons ;.2'
# 103 = {str} 'Participation rate ;  > Males ;'
# 104 = {str} 'Participation rate ;  > Males ;.1'
# 105 = {str} 'Participation rate ;  > Males ;.2'
# 106 = {str} 'Participation rate ;  > Females ;'
# 107 = {str} 'Participation rate ;  > Females ;.1'
# 108 = {str} 'Participation rate ;  > Females ;.2'
# 109 = {str} 'Not in the labour force (NILF) ;  Persons ;'
# 110 = {str} 'Not in the labour force (NILF) ;  > Males ;'
# 111 = {str} 'Not in the labour force (NILF) ;  > Females ;'
# 112 = {str} 'Civilian population aged 15 years and over ;  Persons ;'
# 113 = {str} 'Civilian population aged 15 years and over ;  > Males ;'
# 114 = {str} 'Civilian population aged 15 years and over ;  > Females ;'