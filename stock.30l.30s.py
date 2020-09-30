#!/usr/bin/env python3
import json
import requests

from yahoofinancials import YahooFinancials
from numbers import Number
from datetime import datetime
import time
from forex_python.converter import CurrencyRates

# Stock symbols
stock_symbols_dict = {
  "VALE": 205,
  "NIO": 130,
  "SHLL": 50,
  "AMD": 20,
  "GLPG.AS": 8,
  "HCAC":110,
  "MSFT": 3,
  "AAPL": 4,
  "SEP1": -1,
  "EMIM.AS": 41,
  "VUSA.AS": 4,
  "IWDA.AS": 18,
  "SEP2": -1,
  "TSLA": 0,
  "NET": 0,
  "LAC": 0,
  "PTON": 0
}
market_dict_group = [stock_symbols_dict]
initial_investment = 8637
cash = -4063
#-----------------------------------------------------------------------------

#print('stop')
#exit(0)

start_time = time.time()

result = ""
def prepend_line(string):
  global result
  result = string + "\n" + result
def append_line(string):
  global result
  result = result + string + "\n"
def get_color(value):
  if (value < -0.001):
    return "color='#fc4953'"
  elif (value > 0.001):
    return "color='#3bd972'"
  else:
    return '' #242424
  
append_line("---")

c = CurrencyRates()
usd_rate = c.get_rate("USD","EUR")

total_worth = cash
total_worth_changed = 0

#TODO HEADERS
#append_line("{4:7}<b>{0:6}</b> {1:10} {2:10} {3:11} | font=monospace".format("Symbol","%", "Price", "Δ",""))
append_line("{0:^4} <b>{1:^7}</b>{2:^9}{3:^9}{4:^9}{5:^5}{6:^7}{7:^7} |font=monospace".format("MAR","SYMBOL","%","PRICE","Δ","$","TOTAL","TOTAL Δ"))
append_line("---")
for stock_symbol_dict in market_dict_group:

  stock_symbols = list(stock_symbol_dict.keys())

  data = YahooFinancials(stock_symbols).get_stock_price_data()

  for stock_symbol in stock_symbols:

      if (stock_symbol_dict[stock_symbol] == -1):
        append_line("---")
        continue
     
      try:

        ticker = data[stock_symbol]
        
        amount_owned = stock_symbol_dict[stock_symbol]
        
        currency = "-"
        
        currency = ticker['currencySymbol']
        
        stock_symbol = ticker.get('symbol')
        market_state = ticker.get('marketState')
        if (market_state == 'PREPRE'):
          market_state = 'CLOSED'
        #elif not (market_state.lower() + "MarketChangePercent") in ticker:
        #  market_state = 'CLOSED'
        market_state_lower = market_state.lower()
        
        key_price_current = market_state_lower + 'MarketPrice'
        key_price_change = market_state_lower + 'MarketChange'
        key_price_change_percent = market_state_lower + 'MarketChangePercent'
        
        regular_market_price = ticker.get('regularMarketPrice', 0)
        price_current = ticker.get(key_price_current, regular_market_price)
        if price_current is None:
          price_current = regular_market_price
        price_changed = ticker.get(key_price_change, 0)
        if price_changed is None:
          price_changed = 0
        price_percent_changed = ticker.get(key_price_change_percent, 0) * 100 

        worth = amount_owned * price_current
        worth_changed = amount_owned * price_changed
        
        if (currency == '$'):
          worth = float(worth) * usd_rate
          worth_changed = float(worth_changed) * usd_rate

        total_worth = total_worth + worth
        total_worth_changed = total_worth_changed + worth_changed
        
        color = get_color(price_changed)
        
        append_line("{7:4} <span {6}><b>{4:7}</b> {0:{5}7.2f}% {1:>7.2f} {2:{5}7.2f} {3:5} {8:>7.2f} {9:>5.2f}</span> |font=monospace".format(price_percent_changed,price_current, price_changed, currency, stock_symbol, '+' if price_changed else '', color, market_state[:3], worth, worth_changed))
        
        # Collapsed: all information available
        for key, value in ticker.items():
          if (not value == None):
            append_line ("-- {:30} {} | font=monospace".format(key, value))
      except Exception as e:
        append_line(str(e))
        for key, value in ticker.items():
          if (not value == None):
            append_line ("-- {:30} {} | font=monospace".format(key, value))
        pass
  append_line("---")
  
total_percent_changed = total_worth_changed / total_worth * 100   
all_time_changed = total_worth - initial_investment
all_time_percent_changed = all_time_changed / initial_investment * 100

append_line("Total worth: €{0:.2f}, Delta: €{1:.2f}, {2:+.2f}% | font=monospace".format(total_worth,total_worth_changed, total_percent_changed))
append_line("All time delta: €{0:.2f}, {1:+.2f}% | font=monospace".format( all_time_changed, all_time_percent_changed))
append_line("---")
append_line("Last updated at {}, took {} seconds | font=monospace".format(datetime.now().strftime("%H:%M:%S"), str((round(time.time() - start_time)))))
append_line("---")
append_line("<i>Refresh</i> | refresh=true | iconName=view-refresh")

color = get_color(total_percent_changed)

#prepend_line("Stonks <span {0}>{1:+.2f}%</span>".format(color, total_percent_changed))
prepend_line("Stonks")

print(result)
