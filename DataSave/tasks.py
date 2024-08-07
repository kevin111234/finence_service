import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

from DataSave.exchange_data import dollar_rate, dollar_index
from DataSave.stock_data import ticker_update, stock_data_update, stock_index_update, commodity_data_update

def save_dollar_rate():
    dollar_rate()

def save_dollar_index():
    dollar_index()

def save_stock_ticker():
    ticker_update()

def save_stock_data():
    stock_data_update()

def save_stock_index():
    stock_index_update()

def save_commodity_data():
    commodity_data_update()

if __name__=="__main__":
    save_stock_index()