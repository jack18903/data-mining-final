import pandas as pd
from tslearn.preprocessing import TimeSeriesScalerMeanVariance


if __name__ == '__main__':

    # get file from data.csv and normalize


    df = pd.read_csv('data.csv')

    # because the data of symbols has different number of days, this line must be added
    df.apply(lambda col: col.drop_duplicates().reset_index(drop=True))

    for i, symbol in enumerate(df.columns[1:], start=1):
        print(f'Normalize data: {i}/100')

        close_prices = df[symbol]

        normalized_closes = TimeSeriesScalerMeanVariance(mu=0., std=1.).fit_transform([close_prices])
        normalized_closes = normalized_closes.flatten()

        df[symbol] = pd.Series(normalized_closes)

    df.to_csv('data-normalized.csv', index=False)
