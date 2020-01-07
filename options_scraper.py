import requests
import urllib.request
import datetime
import time
from bs4 import BeautifulSoup

def get_call_data(stock_name, expire_time, strike_price):
    date = time.mktime(datetime.datetime.strptime(expire_time, "%d/%m/%Y").timetuple())+(16*3600)
    url = 'https://finance.yahoo.com/quote/'+stock_name+'/options?date='+str(int(date))+'&p='+stock_name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    values = soup.findAll("td" )

    for i in range(2,len(values),11):
        x = float(str(values[i].contents[0].contents[0]))
        if x == float(strike_price):
            return (float(values[i+2].contents[0]), float(values[i+3].contents[0]))

def get_put_data(stock_name, expire_time, strike_price):
    date = time.mktime(datetime.datetime.strptime(expire_time, "%d/%m/%Y").timetuple())+(16*3600)
    url = 'https://finance.yahoo.com/quote/'+stock_name+'/options?date='+str(int(date))+'&p='+stock_name
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    values = soup.findAll("table")[1].findAll("td")

    for i in range(2,len(values),11):
        x = float(str(values[i].contents[0].contents[0]))
        if x == float(strike_price):
            return (float(values[i+2].contents[0]), float(values[i+3].contents[0]))
