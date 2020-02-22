
# app/robo_advisor.py

# get_data.pyimport requests
import json
import requests
from dotenv import load_dotenv
import os
import csv
import statistics
import datetime
import plotly
import plotly.graph_objects as go
#import pandas


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71



#ToDo Output the desired output to a csv file



#breakpoint()
load_dotenv()
print("REQUESTING SOME DATA FROM THE INTERNET...")

#API_KEY = "PXGNWMUO97DNAVPX"
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS")

symbol = input("Enter a stock ticker to analyze and generate a rec for\t") #TODO ask for a user input



request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)

#handle response errors:

if ("Error Message" in response.text):
    print(f"OOPS couldn't find that symbol {symbol}, please try again")
    exit()



print(response.status_code)



#print(response.text)



parsed_response = json.loads(response.text)

#print(parsed_response) #> list
#breakpoint()
#CSV_fileName = symbol


tsd = parsed_response["Time Series (Daily)"]
#print(tsd)
#print ([d for d in tsd])
#for d in tsd:
    #print(type(tsd))
   # print(type(d["4. close"]))

 #ToDO Sort just to make sure

CSVfilePath = os.path.join(os.path.dirname(__file__), "..", "data", symbol + "stock.csv")

print (os.path.abspath(CSVfilePath))
#breakpoint()
with open (CSVfilePath, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames =["timestamp", "open", "close", "high", "low", "volume"])
    writer.writeheader()
    for dates in tsd:
        writer.writerow({
        "timestamp": dates,
        "open": tsd[dates]["1. open"], 
        "close": tsd[dates]["4. close"], 
        "high": tsd[dates]["2. high"], 
        "low": tsd[dates]["3. low"], 
        "volume": tsd[dates]["5. volume"]
        })
dates = list(tsd.keys())
latest_day = dates[0]
#print (type(latest_day))

latest_close = (tsd[latest_day]["4. close"])
recent_high = (tsd[latest_day]["2. high"])
recent_low = (tsd[latest_day]["3. low"])
#breakpoint()

high_list = []
for date in dates:
    print(type(date))
    high_price = float(tsd[date]["2. high"])
    high_list.append(high_price)

#
#print (high_list)
#breakpoint()

high_price = max(high_list)
print(f"Highest price: {high_price}")

print("-----------------------\n---------------------")
min_list = []
for date in dates:
    min_price = float(tsd[date]["3. low"])
    min_list.append(min_price)



min_price = min(min_list)
print(f"Lowest price: {min_price}")
high_price = float(high_price)
latest_close = float(latest_close)
min_price = float(min_price)


recommendation =""
rec_explanation =""
if latest_close < (0.80 * high_price) and latest_close < (min_price + high_price)/2:
    recommendation = "BUY"
    rec_explanation = "Because the stock has fallen by at least 20% of the recent 100 day high, we recommend a buy of the security"
elif latest_close > 0.80 * high_price and latest_close > (high_price+min_price)/2:
    recommendation = "Sell"
    rec_explanation = "Because the stock is at least 90% of the recent 100 day high, we recommend a sell of the security"
else:
    recommendation = "Hold"
    rec_explanation = "Because the stock's trading sideways "
now = datetime.datetime.now()
request_time = now.strftime("%Y-%m-%d %I:%M %p")


print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {request_time}")
print("-------------------------")
print(f"LATEST DAY: {latest_day}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(high_price))}")
print(f"RECENT LOW: {to_usd(float(min_price))}")
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}!")
print(f"RECOMMENDATION REASON: {rec_explanation}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

dates.sort(reverse=True)
#todo plot graph of the recent prices
#tsd.sort(key = [tsd[d] for d in tsd], reverse = True)
#print (tsd)
plotly.offline.plot({
    "data": [go.Scatter(x=[date for date in tsd], y=[float(tsd[date]["4. close"]) for date in tsd])],
    "layout": go.Layout(title=f"{symbol} Stock Chart")
}, auto_open=True)