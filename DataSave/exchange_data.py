import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

import FinanceDataReader as fdr
from datetime import datetime, timedelta
from DataSave.models import ExchangeRate, DollarIndex
from django.db.models import Max

def update_exchange_rate(base_currency, target_currency):
    print(f"환율 데이터를 업데이트합니다: {base_currency}/{target_currency}")
    
    symbol = f"{base_currency}/{target_currency}"
    try:
        # 해당 통화 쌍의 데이터베이스에 저장된 마지막 날짜를 가져옵니다.
        last_saved_date = ExchangeRate.objects.filter(base_currency=base_currency, target_currency=target_currency).aggregate(Max('date'))['date__max']
        
        if last_saved_date is None:
            # 데이터가 없는 경우 2010년부터 데이터 가져오기
            start_date = datetime.strptime('2010-01-01', '%Y-%m-%d')
        else:
            # 데이터가 있는 경우 마지막 저장된 날짜 이후부터 데이터 가져오기
            start_date = last_saved_date + timedelta(days=1)
        
        # 특정 통화 쌍의 역사적 데이터 가져오기
        exchange_rate_data = fdr.DataReader(symbol, data_source='FOREX', start=start_date.strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'))
        
        for date, data in exchange_rate_data.iterrows():
            ExchangeRate.objects.update_or_create(
                base_currency=base_currency,
                target_currency=target_currency,
                date=date.date(),
                defaults={
                    'open': data['Open'],
                    'high': data['High'],
                    'low': data['Low'],
                    'close': data['Close'],
                    'volume': data.get('Volume', None)  # 볼륨 데이터가 없는 경우도 처리
                }
            )
        print(f"{symbol} 환율 데이터 업데이트 완료")
    except Exception as e:
        print(f"Error saving historical data for {symbol}: {e}")

    print(f"{symbol} 환율 데이터 저장 완료")

def dollar_rate():
    print("환율정보를 저장합니다...")
    currency_pairs = [
        ('USD', 'EUR'),
        ('USD', 'JPY'),
        ('USD', 'GBP'),
        ('USD', 'AUD'),
        ('USD', 'CAD'),
        ('USD', 'CHF')
    ]
    
    for base_currency, target_currency in currency_pairs:
        update_exchange_rate(base_currency, target_currency)

def dollar_index():
    print("달러인덱스를 저장합니다...")
    
    symbol = 'FRED:DTWEXM'  # 달러 인덱스 심볼
    try:
        # 달러 인덱스의 데이터베이스에 저장된 마지막 날짜를 가져옵니다.
        last_saved_date = DollarIndex.objects.aggregate(Max('date'))['date__max']
        
        if last_saved_date is None:
            # 데이터가 없는 경우 2010년부터 데이터 가져오기
            start_date = datetime.strptime('2010-01-01', '%Y-%m-%d')
        else:
            # 데이터가 있는 경우 마지막 저장된 날짜 이후부터 데이터 가져오기
            start_date = last_saved_date + timedelta(days=1)
        
        # 달러 인덱스의 역사적 데이터 가져오기
        dollar_index_data = fdr.DataReader(symbol, start=start_date.strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'))
        
        for date, data in dollar_index_data.iterrows():
            DollarIndex.objects.update_or_create(
                date=date.date(),
                defaults={
                    'close': data['DTWEXM']
                }
            )
        print(f"{symbol} 달러 인덱스 데이터 업데이트 완료")
    except Exception as e:
        print(f"Error saving historical data for {symbol}: {e}")

    print(f"{symbol} 달러 인덱스 데이터 저장 완료")