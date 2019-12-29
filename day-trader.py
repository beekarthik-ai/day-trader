import yfinance as yf
import pickle

class Trader:
    """
    Simulates a trader. Initialized with name, money, and portfolio.
    Can buy, sell, short sell, and short cover stocks. using the function below.
    """
    def __init__(self, name, money):
         self.name = name
         self.portfolio = []
         self.money = money
         all_traders.append(self)

    def buy(self, stock_name, quantity, price):
        assert money >= quantity*price, "Insufficient funds to place order"
        self.money -= quantity*price
        for pos in self.portfolio:
            if pos.name is stock_name and type(pos) != Short:
                pos.add(quantity)
                return
        newPosition = Position(stock_name, quantity)
        self.portfolio.append(newPosition)

    def sell(self, stock_name, quantity, price):
        self.money += quantity*price
        for pos in self.portfolio:
            if pos.name is stock_name:
                pos.subtract(quantity)

    def market_order_buy(self, stock_name, quantity):
        """
        Buy some quantity of a stock for the market ask price at or below the current
        ask size.
        """
        ask_offer = get_ask_offer(stock_name, True)
        assert quantity <= ask_offer[1], 'Quantity desired ({0}) is greater than ask size ({1})'.format(quantity, ask_offer[1])
        self.buy(stock_name, quantity, ask_offer[0])

    def market_order_sell(self, stock_name, quantity):
        """
        Sell some quantity of a stock for the market bid price at or below the current
        bid size.
        """
        bid_offer = get_bid_offer(stock_name, True)
        assert quantity <= bid_offer[1], 'Quantity desired ({0}) is greater than ask size ({1})'.format(quantity, bid_offer[1])
        self.buy(stock_name, quantity, bid_offer[0])

    def short_sell(self, stock_name, quantity):
        """
        Short sell some quantity of stock for the current bid price at or below the current
        bid size.
        """
        self.money += quantity*get_bid_offer(stock_name, True)[0]
        for pos in self.portfolio:
            if pos.name is stock_name and type(pos) == Short:
                pos.add(quantity)
                return
        newShort = Short(stock_name, quantity)
        self.portfolio.append(newShort)

    def short_cover(self, stock_name, quantity):
        """
        Cover some quantity of stock for the current ask price at or below the current
        ask size.
        """
        for pos in self.portfolio:
            if pos.name is stock_name and type(pos) == Position:
                long_pos = pos
            if pos.name is stock_name and type(pos) == Short:
                short_pos = pos
        assert long_pos.quantity >= quantity, 'Not enough stock to cover desired quantity'
        long_pos.subtract(quantity)
        short_pos.subtract(quantity)

class Position:
    """
    Represents a basic long position of a security
    """
    updateNeeded = False
    def __init__(self, name, quantity):
        self.name = name
        self.ticker = yf.Ticker(name)
        self.quantity = quantity
    def add(self, amount):
        self.quantity += amount
    def subtract(self, amount):
        self.quantity-=amount
        if self.quantity == 0:
            del self
    def __repr__(self):
        return (self.name, self.quantity, type(self))

class Short(Position):
    """
    Represents a short position of a security
    """
    def __init__(self, name, quantity):
        super().__init__(name, quantity)
        self.borrow_fee = get_borrowing_fee(stock_name)

def get_borrowing_fee(stock_name):
    return

def get_ask_offer(stock_name, return_values=False):
    info = yf.Ticker(stock_name).info
    if return_values:
        return info['ask'], info['askSize']
    return '${0} x {1}'.format(info['ask'], info['askSize'])

def get_bid_offer(stock_name, return_values=False):
    info = yf.Ticker(stock_name).info
    if return_values:
        return info['bid'], info['bidSize']
    return '${0} x {1}'.format(info['bid'], info['bidSize'])

###################
# Analysis Tools #
##################

"""
Fundamental and technical analysis tools coming in future versions
"""

#######################################
# Saving and loading Trading accounts #
#######################################

all_traders = []
all_file_names = []

def save(trader):
    """
    Saves a trader object into a bytestream using the Python pickle module
    """
    file_name=trader.name+'.p'
    file_path = './pickled_data/'

    if file_name in all_file_names:
        print("A file with the name {0}, would you like to overwrite that file?".format(file_name))
        input = raw_input("Yes/No: ")
        if input.lower() is 'yes':
            pickle.dump(trader, open(file_path+file_name, 'wb'))
    else:
        pickle.dump(trader, open(file_path+file_name, 'wb'))
        all_file_names.append(file_name)
    pickle.dump(all_file_names, open(file_path+'all_file_names.p', 'wb'))

def load(file_name):
    """
    Returns the trader object contained within a file
    """
    file_path = './pickled_data/'
    return pickle.load(open(file_path+file_name, 'rb'))

####################################
#Loads data from previous sessions #
####################################

if __name__ == '__main__':
    all_file_names = pickle.load(open('./pickled_data/all_file_names.p', 'rb'))
