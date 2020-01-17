import requests
import urllib.request
import datetime
import time
from bs4 import BeautifulSoup

"""
The functions below scrape the Yahoo Finance website, and return the ask and bid
for a stock at a particular strike price, for a certain week. Note that the expire_time
must be a string of the form DD/MM/YYYY where the day is a Thursday. Hopefully next version
will have a better way of specifying the expire date.
"""
def get_call_data(stock_name, expire_time, strike_price):
    """
    Returns a tuple containing the bid price and ask price of a call option
    """
    date = time.mktime(datetime.datetime.strptime(expire_time, "%d/%m/%Y").timetuple())+(16*3600)
    url = 'https://finance.yahoo.com/quote/'+stock_name+'/options?date='+str(int(date))+'&p='+stock_name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    values = soup.findAll("td" )

    for i in range(2,len(values),11):
        x = float(str(values[i].contents[0].contents[0]))
        if x == float(strike_price):
            option_link = 'https://finance.yahoo.com/'+str(values[i-2].contents[0])[61:109]
            bid = float(values[i+2].contents[0])
            ask = float(values[i+3].contents[0])
            return bid, ask

def get_put_data(stock_name, expire_time, strike_price):
    """
    Returns a tuple containing the bid price and ask price of a put option
    """
    date = time.mktime(datetime.datetime.strptime(expire_time, "%d/%m/%Y").timetuple())+(16*3600)
    url = 'https://finance.yahoo.com/quote/'+stock_name+'/options?date='+str(int(date))+'&p='+stock_name
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    values = soup.findAll("table")[1].findAll("td")

    for i in range(2,len(values),11):
        x = float(str(values[i].contents[0].contents[0]))
        if x == float(strike_price):
            option_link = 'https://finance.yahoo.com/'+str(values[i-2].contents[0])[61:109]
            bid = float(values[i+2].contents[0])
            ask = float(values[i+3].contents[0])
            return bid, ask
