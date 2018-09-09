from iexfinance import get_available_symbols
import pandas as pd
from collections import Counter
from .tools import clean, remove_punctuation


class TickerSearch:
    def __init__(self):
        self.ticker_dataframe = self._fetch_all_iex_tickers()

    def _fetch_all_iex_tickers(self):
        columns = ['symbol', 'name']
        df = pd.DataFrame(get_available_symbols())
        df = df[df.isEnabled == True]
        df = df[df.type != 'crypto']
        df = df[df.name != 'NASDAQ TEST STOCK']
        df = df.set_index('iexId')
        return df[columns]

    @property
    def all_symbols(self):
        symbols = self.ticker_dataframe['symbol']
        return symbols

    @property
    def all_names(self):
        series = self.ticker_dataframe['name']
        empty = series != ''
        return series[empty]

    @property
    def all_strings(self):
        all_strings = []
        for group in self.all_names.apply(clean):
            all_strings += group
        c = Counter(all_strings)
        filtered = [x for x in c if c[x] == 1]
        symbols = [clean(symbol)[0] for symbol in self.all_symbols]
        symbols = list(set(symbols))
        return filtered + symbols

    def fuzzy_search(self, word):
        for idx, row in self.all_names.iteritems():
            if word in row:
                return self.ticker_dataframe.loc[str(idx)]

        return pd.Series()

    def __getitem__(self, index):
        df = self.ticker_dataframe
        index = index.upper()
        try:
            return df.loc[str(index).upper()]
        except KeyError:
            pass

        name = df[df['name'] == str(index)]
        symbol = df[df['symbol'] == str(index)]
        fuzzy = self.fuzzy_search(index)

        if len(name) > 0:
            return name
        elif len(symbol) > 0:
            idx = symbol.index[0]
            return self.ticker_dataframe.loc[str(idx)]
        elif len(fuzzy) > 0:
            return fuzzy
        else:
            raise KeyError(f'{index} not found.')

#
# #
# from random import choice
# TS = TickerSearch()
# for _ in range(100):
#     found_word = choice(TS.all_strings)
#     try:
#         print(TS[found_word])
#     except KeyError:
#         pass
