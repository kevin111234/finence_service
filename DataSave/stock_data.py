import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

def ticker_update():
    print("티커 데이터를 업데이트합니다...")

def stock_data_update():
    print("주가 데이터를 업데이트합니다...")

def stock_index_update():
    print("시장 지수 데이터를 업데이트합니다...")