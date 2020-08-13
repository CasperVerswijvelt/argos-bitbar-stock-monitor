#!/usr/bin/env python3
import json
import requests
import yfinance as yf
from yahoofinancials import YahooFinancials
from numbers import Number

# Enter your stock symbols here in the format: ["symbol1", "symbol2", ...]
stock_symbols_eu = ["BAR.BR", "EURN"]
stock_symbols_us = ["AMD", "RDHL", "INTC", "KODK", "TSLA", "SPCE","AAPL","AMZN"]
markets = [stock_symbols_eu, stock_symbols_us]
#-----------------------------------------------------------------------------

print("Stonks")
print("---")

#TODO HEADERS
#print("<b>{0:6}</b> {1:10} {2:10} {3:11}".format("Symbol","%", "Price", "Δ"))
for stock_symbols in markets:

  data = YahooFinancials(stock_symbols).get_stock_price_data()

  for stock_symbol in stock_symbols:
      
      try:

        ticker = data[stock_symbol]
        
        #for key, value in ticker.items():
        	#if(isinstance(value, Number)and int(value) == 82):
          #print (key, value)
        
        currency = ticker['currencySymbol']
        previousClose = ticker['regularMarketPreviousClose']
        
        stock_symbol = ticker['symbol']
        price_current = ticker['regularMarketPrice']
        price_changed = ticker['regularMarketChange']
        price_percent_changed = ticker['regularMarketChangePercent'] * 100
        color = '#cc575d' if price_changed < 0 else '#d19a66' if price_changed > 0 else '#68b382'
        
        print("<b>{4:6}</b> <span color='{6}'>{0:{5}7.2f}% {1:>7.2f} {2:{5}7.2f} {3:5}</span> |font=monospace".format(price_percent_changed,price_current, price_changed, currency, stock_symbol, '+' if price_changed else '', color))
        for key, value in ticker.items():
          if (not value == None):
            print ("-- {:30} {} | font=monospace".format(key, value))
      except Exception as e:
        print(e)
        pass 
  print("---")
   
print("---")
print("<i>Refresh</i> | refresh=true | iconName=view-refresh")
