import pandas as pd
from tqdm import tqdm

symbols = {'PEARLS':'AMETHYSTS', 'BANANAS':'STARFRUIT'}

class training_data:
    def get_files(self):
        prices = pd.DataFrame()
        trades = pd.DataFrame()
        path = 'backtest-imc-prosperity-2024/training/2023/'
        for day in range(first_day, first_day+3):
            df2 = pd.read_csv(path + f'prices_round_{round}_day_{day}.csv', delimiter=';')
            df3 = pd.read_csv(path + f'trades_round_{round}_day_{day}_nn.csv', delimiter=';')
            df2['timestamp'] += (day - first_day) * 1000000 
            df3['timestamp'] += (day - first_day) * 1000000
            prices = pd.concat([prices,df2], ignore_index=True)
            trades = pd.concat([trades,df3], ignore_index=True)

        for ind in tqdm(prices.index):
            # Replace 2023 products with 2024
            prices.loc[ind,'product'] = symbols[prices['product'][ind]]
        
        for ind in tqdm(trades.index):
            # Replace 2023 products with 2024
            trades.loc[ind,'symbol'] = symbols[trades['symbol'][ind]]

        prices.to_csv(f'prices_round_{round}.csv', index=False, header=True)
        trades.to_csv(f'trades_round_{round}_nn.csv', index=False, header=True)

if __name__ == "__main__":
    round = int(input("Input a round (blank for 1): ") or 1)
    first_day = int(input("Input the first day (blank for 0): ") or 0)
    generate = training_data()
    generate.get_files()