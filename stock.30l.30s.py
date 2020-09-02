#!/usr/bin/env python3
import json
import requests
import yfinance as yf
from yahoofinancials import YahooFinancials
from numbers import Number
from datetime import datetime
import time
from forex_python.converter import CurrencyRates

# Stock symbols
stock_symbols_eu = ["BAR.BR"]
stock_symbols_us = ["TSLA", "PTON", "AMD", "MSFT", "AAPL", "SPCE","INTC","AMZN"]
stock_symbols_dict = {
  "BAR.BR": 29,
  "TSLA": 5,
  "PTON": 24,
  "AMD": 13,
  "MSFT": 3,
  "AAPL": 4,
  "SPCE": 0,
  "INTC": 0,
}
markets = [stock_symbols_eu, stock_symbols_us]
market_dict_group = [stock_symbols_dict]
#-----------------------------------------------------------------------------

start_time = time.time()

print("Stonks")
print("---")

c = CurrencyRates()
usd_rate = c.get_rate("USD","EUR")

total_worth = 0
total_worth_changed = 0

#TODO HEADERS
#print("{4:7}<b>{0:6}</b> {1:10} {2:10} {3:11} | font=monospace".format("Symbol","%", "Price", "Δ",""))
print("{0:^4} <b>{1:^6}</b>{2:^9}{3:^9}{4:^9}{5:^5}{6:^7}{7:^7} |font=monospace".format("MAR","SYMBOL","%","PRICE","Δ","$","TOTAL","TOTAL Δ"))
print("---")
for stock_symbol_dict in market_dict_group:

  stock_symbols = list(stock_symbol_dict.keys())

  data = YahooFinancials(stock_symbols).get_stock_price_data()

  for stock_symbol in stock_symbols:
      
      try:

        ticker = data[stock_symbol]
        
        amount_owned = stock_symbol_dict[stock_symbol]
        
        currency = "-"
        
        
        currency = ticker['currencySymbol']
        
        stock_symbol = ticker['symbol']
        market_state = ticker['marketState']
        if (market_state == 'PREPRE'):
          market_state = 'POST'
        market_state_lower = market_state.lower()
        
        
        key_price_current = market_state_lower + 'MarketPrice'
        key_price_change = market_state_lower + 'MarketChange'
        key_price_change_percent = market_state_lower + 'MarketChangePercent'
        
        price_current = ticker[key_price_current]
        price_changed = ticker[key_price_change]
        price_percent_changed = ticker[key_price_change_percent] * 100 


        worth = amount_owned * price_current
        worth_changed = amount_owned * price_changed

        if (currency == '$'):
          worth = worth * usd_rate
          worth_changed = worth_changed * usd_rate

        total_worth = total_worth + worth
        total_worth_changed = total_worth_changed + worth_changed
        
        color = '#cc575d' if price_changed < 0 else '#d19a66' if price_changed > 0 else '#68b382'
        
        print("{7:4} <b>{4:6}</b> <span color='{6}'>{0:{5}7.2f}% {1:>7.2f} {2:{5}7.2f} {3:5} {8:5.2f} {9:5.2f}</span> |font=monospace".format(price_percent_changed,price_current, price_changed, currency, stock_symbol, '+' if price_changed else '', color, market_state[:3], worth, worth_changed))
        
        # Collapsed: all information available
        for key, value in ticker.items():
          if (not value == None):
            print ("-- {:30} {} | font=monospace".format(key, value))
      except Exception as e:
        print(e)
        pass 
  print("---")
   
print("Total worth: €{0:.2f}, Delta: €{1:.2f} | font=monospace".format(total_worth,total_worth_changed))
print("---")
print("Last updated at {}, took {} seconds | font=monospace".format(datetime.now().strftime("%H:%M:%S"), str((round(time.time() - start_time)))))
print("---")
print("<i>Refresh</i> | refresh=true | iconName=view-refresh")
