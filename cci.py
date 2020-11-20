from backend.data_tools import CoinSearch, DataHandler

if __name__ == '__main__':
    cs = CoinSearch()
    cs.search_for_coin('snx')

    dh = DataHandler()
    dh.calculate_returns()
