# Notes and Credit

This is a backtester based originally on the 2023 backtester built by n-0 (https://github.com/n-0/backtest-imc-prosperity-2023/)
It's reasonably heavily modified to work with the 2024 format and the stock jmerle logger (no modifications required).
A slightly modified datamodel is included, but all traders that compile with it should be fully compatible with the required format.

I've also included my own concatenation tool for joining multiple days data into a single dataset, such as can be found in the 2023 training data sets.

# Backtest IMC Prosperity 2024

This is repo contains utilities for IMC Prosperity 2024 challenge.
Right now, it has the [backtester.py](./backtester.py), that should mimic log files from
the prosperity challenge [platform](https://prosperity.imc.com/).
The format is good enough to be accepted by jmerle's amazing [project](https://github.com/jmerle/imc-prosperity-2-visualizer),
for visualizing the order book as well as your trades.

## Order matching
Orders returned by the `Trader.run` method, are matched against the `OrderDepth`
of the state provided to the method call. The trader always gets their trade and
trades from bots are ignored. An order is matched only if the price is exactly the
same as an opposite one from `OrderDepth`. If the new position that would result from
this order exceeds the specified limit of the symbol, all following orders (including the failing one)
are cancelled. You can relax those conditions by answering sth. to `Matching orders halfway (sth. not blank for True):`, during the input dialog
of the backtester. Halfway matches any volume (regardless of order book), such that
sell/buy orders are always matched, if they're below/above the midprice
of the highest bid/lowest ask (regardless of volume).
If an order couldn't be matched the backtester will look the current order depth and your unmatched order.

## After All
If your trader has a method called `after_last_round`, it will be called after the logs have been written.
This is useful for plotting something with matplotlib for example (but don't forget to remove the import,
when you upload your algorithm).

## General usage
Add the csv's from IMC to the training folder and adjust if necessary the constant `TRAINING_DATA_PREFIX`
to the full path of `training` directory on your system, at the top of `backtester.py`.
Import your Trader at the top of `backtester.py` (in the repo the Trader from `dontlooseshells.py` is used).
Then run
```bash
python backtester.py
```
This executes
```
if __name__ == "__main__":
    trader = Trader()
    simulate_alternative(3, 0, trader, False, 30000)
```
The central method is `simulate_alternative`. There are some default parameters
and the meaning is
```
def simulate_alternative(
        round: int, 
        day: int, 
        trader, 
        time_limit=1e8, 
        names=True, 
        halfway=False,
        monkeys=False,
        monkey_names=['Max', 'Camilla']
    ):
```
where round and day are substituted to the following path `{TRAINING_DATA_PREFIX}/prices_round_{round}_day_{day}.csv` (same for `trades_round...`).
Trader is your algorithm trader, `time_limit` can be decreased to only read a part of the full training file. `names` reads the training files with names on `market_trades`. `halfway` enables smarter order matching.

## Logging with jmerle's visualizer
A working example is given in [dontlooseshells.py](./dontlooseshells.py).


## Profit and Loss (PnL)
PnL is maintained via four time series
 
* `profits_by_symbol` (the final pnl)
* `balance_by_symbol:` (credit_by_symbol + unrealized_by_symbol) 
* `credit_by_symbol:` (the amount of credit you had to take to open up the position (opposite sign of trade.quantity))
* `unrealized_by_symbol:` (the approximated value (mid price) if you would close the position at this point in time) 
PnL is calculated if your position of some asset is changed to 0, by a trade. Until then credit_by_symbol holds
the amount of the previous executed trades and the amount of seashells you borrowed (both short and long require borrowing Because
you're not trading on the profits or some initial balance of your previous competition rounds). On closing your whole position credit_by_symbol
will only contain the pnl and is added to profits_by_symbol. This would not give you enough information to evaluate your current portfolio between trades, hence 
the need for balance_by_symbol. For the logger file balance_by_symbol is added to profits_by_symbol, which gives similar values to the simulation. 
Be aware that the IMC environment matches more trades, than the backtester, thus the final values might be different. But if exactly the same trades
would be executed then both give the same results.


The value of an executed trade is:
```python
current_pnl += -trade.price * trade.quantity
```
Meaning that if the trade was selling a symbol (e.g. Shorting) the trade.quantity is negative ,
ending in a positive `current_pnl`. Hence buying a symbol is a positive trade.quantity, ending in a negative `current_pnl`.


Good luck 🍀
