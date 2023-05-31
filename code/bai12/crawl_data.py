import os
import pandas as pd
from src.api import get_stock_symbols, get_symbol_data
from constant import *

if __name__ == '__main__':    
    symbols = get_stock_symbols()

    df = pd.DataFrame({}, columns=[COL_DATE, *symbols])

    # because the data of symbols has different number of days, this line must be added
    df.apply(lambda col: col.drop_duplicates().reset_index(drop=True))

    for i, symbol in enumerate(symbols, start=1):
        print(f'Get symbol data: {i}/100')

        data = get_symbol_data(symbol)

        if i == 1:
            df[COL_DATE] = data.keys()

        df[symbol] = pd.Series(data.values())

    df.to_csv(os.path.join('data.csv'), index=False, sep=',')