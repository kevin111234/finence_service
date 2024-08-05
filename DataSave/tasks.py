import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

from DataSave.exchange_data import dollar_rate, dollar_index
from DataSave.stock_data import ticker_update, stock_data_update, stock_index_update
