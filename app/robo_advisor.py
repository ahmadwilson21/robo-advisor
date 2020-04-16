
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


load_dotenv()
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS") #Gets API key from .env file
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

def dash_attack():
    """
    Returns assortment of dashes to separate lines of output
    Example: dash_attack()
    Returns: "-------------------------"
    """
    return "-------------------------"

def compile_url(symbol):
    """
    Takes stock ticker, navigates to alphavantage website and returns the website's status code
    Example: compile_url("MSFT")
    Returns: 202
    """

    if (symbol.isalpha() == False or len(symbol)>5): 
        print(f"OOPS couldn't find that symbol {symbol}, please try again")
        exit()
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    
    response = requests.get(request_url)
    return response.status_code

def get_response(symbol):
    """
    Navigates to alphavantage website with specific ticker and returns the stock info in 
    dictionary format
    Example: [get_response("MSFT").keys()]
    Return: ["Time Series(Daily", "Meta Data"]
    """
    
    if compile_url(symbol) != 200:
        print(f"OOPS couldn't reach website, please try again")
        exit()
    
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    

    return parsed_response 



def calculate_prices(parsed_response):
    """
    Generates list of formatted dictionaies with the stock information from the website
    Example: 
    parsed_response = {
        "Time Series (Daily)": {
            "2019-06-08": {
                "1. open": "101.0924",
                "2. high": "101.9500",
                "3. low": "100.5400",
                "4. close": "101.6300",
                "5. volume": "22165128"
            },
            "2019-06-07": {
                "1. open": "102.6500",
                "2. high": "102.6900",
                "3. low": "100.3800",
                "4. close": "100.8800",
                "5. volume": "28232197"
            },
            "2019-06-06": {
                "1. open": "102.4800",
                "2. high": "102.6000",
                "3. low": "101.9000",
                "4. close": "102.4900",
                "5. volume": "21122917"
            }
        }
    
    calculate_prices(parsed_response)

    returns: [
        {"timestamp": "2019-06-08", "open": 101.0924, "high": 101.95, "low": 100.54, "close": 101.63, "volume": 22165128},
        {"timestamp": "2019-06-07", "open": 102.65, "high": 102.69, "low": 100.38, "close": 100.88, "volume": 28232197},
        {"timestamp": "2019-06-06", "open": 102.48, "high": 102.60, "low": 101.90, "close": 102.49, "volume": 21122917}     
        ]
        
    """

    tsd = parsed_response["Time Series (Daily)"]
    rows = []

    for date, daily_prices in tsd.items():
        row = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])     
        }
        rows.append(row)
 
    return rows


def write_to_csv(rows, csv_filepath):
    """
    Generates csv file with dictionaries of stock data captured from the alphavantage website
    Example: 
    response = [ {"timestamp": "2019-06-08", "open": 101.0924, "high": 101.95, "low": 100.54, "close": 101.63, "volume": 22165128},
        {"timestamp": "2019-06-07", "open": 102.65, "high": 102.69, "low": 100.38, "close": 100.88, "volume": 28232197},
        {"timestamp": "2019-06-06", "open": 102.48, "high": 102.60, "low": 101.90, "close": 102.49, "volume": 21122917},
    ]
    write_to_csv(response, "Users/Downloads/price.csv")

    Returns True
    """

    with open (csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames =["timestamp", "open", "close", "high", "low", "volume"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        print([row for row in reader])
        
    
    return True
        











if __name__ == "__main__":
    from send_email import sendEmail

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


    symbol = (input("Enter a stock ticker to analyze and generate a rec for\t")).upper() #aks user for stock ticker

    parsed_response = get_response(symbol)

    latest_day = parsed_response["Meta Data"]["3. Last Refreshed"]
    rows = calculate_prices(parsed_response)

    latest_close = rows[0]["close"]
    high_prices = [row["high"] for row in rows] # list comprehension for mapping purposes!
    low_prices = [row["low"] for row in rows] # list comprehension for mapping purposes!
    recent_high = max(high_prices)
    recent_low = min(low_prices)

    CSVfilePath = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" +symbol + ".csv")
    write_to_csv(rows, CSVfilePath)

    tsd = parsed_response["Time Series (Daily)"]#accesses the stock's information across 100 days
    dates = list(tsd.keys()) #adds dates to a list so that we can access stock info from specific dates (ie. today and yesterday)
    latest_day = dates[0] #provides access to today's stock info
    penultimate_day = dates[1] #provides access to yesterday's stock info


    high_price = float(recent_high)
    latest_close = float(latest_close)
    min_price = float(recent_low)


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
    print(dash_attack())
    print(f"SELECTED SYMBOL: {symbol}")
    print(dash_attack())
    print("REQUESTING STOCK MARKET DATA...")
    print(f"REQUEST AT: {request_time}")
    print(dash_attack())
    print(f"LATEST DAY: {latest_day}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(high_price))}")
    print(f"RECENT LOW: {to_usd(float(min_price))}")
    print(dash_attack())
    print(f"RECOMMENDATION: {recommendation}!")
    print(f"RECOMMENDATION REASON: {rec_explanation}")
    print(dash_attack())
    print("HAPPY INVESTING!")
    print(dash_attack())



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


