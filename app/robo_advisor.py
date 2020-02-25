
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
from send_email import *

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


load_dotenv()

#Asks user for preliminary info necessary for sending email updates
email_flag = False #flag that lets program know if we need to send an email or not
to_email = "abc@gmail.com"#Email for sending the updates to 
email_prompt = (input("Would you like to receive Email notifications for fluctuations in price? (y/n)\t")).upper()
if (email_prompt == "Y"):
    email_flag = True
    to_email = input("Enter your email address\t(abc@email.com)\t")
else:
    print("No emails will be sent")



print("REQUESTING SOME DATA FROM THE INTERNET...")

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS") #Gets API key from .env file

symbol = (input("Enter a stock ticker to analyze and generate a rec for\t")).upper() #aks user for stock ticker

#Checks to see if the symbol is not a string of characters, so if it has any numbers then it will ouput an error
if (symbol.isalpha() == False or len(symbol)>5): 
    print(f"OOPS couldn't find that symbol {symbol}, please try again")
    exit()

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"#URL/API for requesting the stock data

response = requests.get(request_url)


#Exits the program if there are any response errors:
if ("Error Message" in response.text):
    print(f"OOPS problem with retrieving the website url, please try again")
    exit()




parsed_response = json.loads(response.text) #converts json into python dictionary


tsd = parsed_response["Time Series (Daily)"]#accesses the stock's information across 100 days

#Creates filepath for the eventual csv file inside of a folder called data
CSVfilePath = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" +symbol + ".csv")

#Writes each date's stock info for the last 100 days into a csv file
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
dates = list(tsd.keys()) #adds dates to a list so that we can access stock info from specific dates (ie. today and yesterday)
latest_day = dates[0] #provides access to today's stock info
penultimate_day = dates[1] #provides access to yesterday's stock info


latest_close = (tsd[latest_day]["4. close"])#The most recent closing price of the security



high_list = [] #list holds all of the recent highs
for date in dates:
    high_price = float(tsd[date]["2. high"])
    high_list.append(high_price)
high_price = max(high_list) #retrieves the highest value from the list of recent highs


min_list = []#list holds all of the recent lows
for date in dates:
    min_price = float(tsd[date]["3. low"])
    min_list.append(min_price)
min_price = min(min_list)#retrieves the lowest value from the list of recent lows


high_price = float(high_price)
latest_close = float(latest_close)
min_price = float(min_price)


"""Recommendation Generation
Generates rec based on if the latest close price is greater than (sell) or less than (buy)
80% of the recent high. Also has a hold recommendation if the stock's recent highs and lows
are relatively the same
"""
recommendation =""
rec_explanation =""
if latest_close < (0.80 * high_price) and latest_close < (min_price + high_price)/2:
    recommendation = "BUY"
    rec_explanation = "Because the stock has fallen by at least 20% of the recent 100 day high, we recommend a buy of the security"
elif latest_close > 0.80 * high_price and latest_close > (high_price+min_price)/2:
    recommendation = "Sell"
    rec_explanation = "Because the stock is at least 80% of the recent 100 day high, we recommend a sell of the security"
else:
    recommendation = "Hold"
    rec_explanation = "Because the stock's trading sideways "
now = datetime.datetime.now()
request_time = now.strftime("%Y-%m-%d %I:%M %p")



#This prompt provies info on the stock's recent prices and provides buy/sell/hold recommendation
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



#This plots the stock data in a line chart over the previous 100 days
plotly.offline.plot({
    "data": [go.Scatter(x=[date for date in tsd], y=[float(tsd[date]["4. close"]) for date in tsd])],
    "layout": go.Layout(title=f"{symbol} Stock Chart")
}, auto_open=True)

if(email_flag == True):
    new_price = float(tsd[latest_day]["4. close"]) #Today's close price
    prev_price = float(tsd[penultimate_day]["4. close"]) #Yesterday's close price
    
    #If today's price is 5% greater than yesterday's close then send an email
    if new_price> prev_price*1.05: #daily rise by 0.5%
        percent_growth=float((new_price-prev_price)/prev_price)
        prompt = f"From Robo Advisor\n\nThe stock {symbol} has risen by {(percent_growth*100):.2f}%\nHappy Investing!"
        sendEmail(to_email,prompt,email_subject=f"{symbol} Up Today")

    #If today's price is 5% less than yesterday's close then send an email
    elif new_price< prev_price*.95: #daily fall by 0.5%
        percent_growth=float((new_price-prev_price)/prev_price)
        prompt = f"From Robo Advisor\n\nThe stock {symbol} has fallen by {(-percent_growth*100):.2f}%\nHappy Investing!"
        sendEmail(to_email,prompt,email_subject=f"{symbol} Down Today")    
    

#Modify the logic of your application such that if it detects the stock's price has moved past
#a given threshold within a given time period (e.g. the price has increased or decreased by more
#than 5% within the past day), it will send the user a "Price Movement Alert" message via email.