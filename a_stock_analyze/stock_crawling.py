import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

import FinanceDataReader as fdr
from datetime import datetime, timedelta
from a_stock_analyze.models import Stock, HistoricalStockData
from django.db.models import Max

def ticker_update():
    us_stocks = fdr.StockListing('NASDAQ')
    for _, row in us_stocks.iterrows():
        symbol = row['Symbol']
        name = row['Name']
        industry_code = row['IndustryCode']
        industry = row['Industry']
        exchange = 'NASDAQ'
        currency = 'USD'
        stock_obj, created = Stock.objects.get_or_create(
            symbol=symbol,
            defaults={
                'name': name,
                'industry_code': industry_code,
                'industry': industry,
                'exchange': exchange,
                'currency': currency
            }
        )
        
        if not created:
            stock_obj.name = name
            stock_obj.industry_code = industry_code
            stock_obj.industry = industry
            stock_obj.exchange = exchange
            stock_obj.currency = currency
            stock_obj.save()

    print("미국 주식 심볼 및 산업 정보 저장 완료")

def save_historical_stock_data():
    # 데이터베이스에서 모든 주식을 가져옵니다.
    stocks = Stock.objects.all()
    
    for stock in stocks:
        try:
            # 해당 주식의 데이터베이스에 저장된 마지막 날짜를 가져옵니다.
            last_saved_date = HistoricalStockData.objects.filter(stock=stock).aggregate(Max('date'))['date__max']
            
            if last_saved_date is None:
                # 데이터가 없는 경우 2013년부터 데이터 가져오기
                start_date = datetime.strptime('2013-01-01', '%Y-%m-%d')
            else:
                # 데이터가 있는 경우 마지막 저장된 날짜 이후부터 데이터 가져오기
                start_date = last_saved_date + timedelta(days=1)
            
            # 특정 주식의 역사적 데이터 가져오기
            stock_data = fdr.DataReader(stock.symbol, start=start_date.strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'))
            
            for date, data in stock_data.iterrows():
                HistoricalStockData.objects.update_or_create(
                    stock=stock,
                    date=date.date(),
                    defaults={
                        'open': data['Open'],
                        'high': data['High'],
                        'low': data['Low'],
                        'close': data['Close'],
                        'volume': data['Volume']
                    }
                )
            print(f'{stock.symbol} 주가 데이터 업데이트 완료')
        except Exception as e:
            print(f"Error saving historical data for {stock.symbol}: {e}")
        
    print("미국 주식의 역사적 데이터 저장 완료")