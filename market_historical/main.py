from market_historical.utils.HistoricalAnalyseClass import HistoricalAnalyseClass
from market_historical.utils.HistoricalGetClass import HistoricalGetClass

if __name__ == '__main__':
    hc = HistoricalGetClass()

    # GET USA DATA
    # hc.get_usa_unemployment()
    # hc.get_usa_fund_rate()
    # hc.get_usa_core_inflation()
    # hc.get_usa_nyse()
    hc.get_usa_nasdaq()

    # ANALYSE DATA
    hac = HistoricalAnalyseClass()

    hac.combine_data()

    hac.analyse_data()