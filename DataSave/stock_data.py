import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

import FinanceDataReader as fdr
from datetime import datetime, timedelta
from django.db.models import Max
from DataSave.models import Stock, HistoricalStockData, StockIndex, HistoricalStockIndexData, Commodity, HistoricalCommodityData

def ticker_update():
    print("티커 데이터를 업데이트합니다...")
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

def stock_data_update():
    print("주가 데이터를 업데이트합니다...")
    # 데이터베이스에서 모든 주식을 가져옵니다.
    stocks = Stock.objects.all()
    
    for stock in stocks:
        try:
            # 해당 주식의 데이터베이스에 저장된 마지막 날짜를 가져옵니다.
            last_saved_date = HistoricalStockData.objects.filter(stock=stock).aggregate(Max('date'))['date__max']
            
            if last_saved_date is None:
                # 데이터가 없는 경우 2010년부터 데이터 가져오기
                start_date = datetime.strptime('2010-01-01', '%Y-%m-%d')
            else:
                # 데이터가 있는 경우 마지막 저장된 날짜 이후부터 데이터 가져오기
                start_date = last_saved_date + timedelta(days=1)
            
            # 특정 주식의 역사적 데이터 가져오기
            stock_data = fdr.DataReader(stock.symbol, start=start_date.strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'))
            stock_data = stock_data.fillna(0, inplace=True)
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

def stock_index_update():
    print("시장 지수 데이터를 업데이트합니다...")
    indices = [
        # 미국
        {'symbol': '^IXIC', 'name': 'NASDAQ Composite'},  # 나스닥 종합 지수: 주로 기술주 중심의 지수
        {'symbol': '^DJI', 'name': 'Dow Jones Industrial Average'},  # 다우존스 산업평균지수: 30개의 주요 블루칩 주식 지수
        {'symbol': '^GSPC', 'name': 'S&P 500'},  # S&P 500: 미국 500대 기업의 주식으로 구성된 지수
        {'symbol': '^RUT', 'name': 'Russell 2000'},  # 러셀 2000: 미국 소형주 중심의 지수
        # 일본
        {'symbol': '^N225', 'name': 'Nikkei 225'},  # 닛케이 225: 일본 도쿄 증권거래소 상장된 225개 대기업의 주가 지수
        # 영국
        {'symbol': '^FTSE', 'name': 'FTSE 100'},  # FTSE 100: 런던 증권거래소에 상장된 시가총액 상위 100개 기업의 지수
        # 독일
        {'symbol': '^GDAXI', 'name': 'DAX'},  # DAX: 독일 프랑크푸르트 증권거래소에 상장된 30개 주요 기업의 지수
        # 프랑스
        {'symbol': '^FCHI', 'name': 'CAC 40'},  # CAC 40: 프랑스 파리 증권거래소에 상장된 40개 주요 기업의 지수
        # 홍콩
        {'symbol': '^HSI', 'name': 'Hang Seng Index'},  # 항셍 지수: 홍콩 증권거래소에 상장된 50개 주요 기업의 주가 지수
        # 중국
        {'symbol': '000001.SS', 'name': 'Shanghai Composite'},  # 상하이 종합 지수: 상하이 증권거래소에 상장된 모든 주식의 지수
        # 한국
        {'symbol': '^KS11', 'name': 'KOSPI'},  # 코스피: 한국 거래소에 상장된 모든 주식의 지수
        # 호주
        {'symbol': '^AXJO', 'name': 'S&P/ASX 200'},  # S&P/ASX 200: 호주 증권거래소에 상장된 200개 주요 기업의 지수
        # 섹터별 지수 (미국)
        {'symbol': '^SP500-45', 'name': 'S&P 500 Information Technology'},  # S&P 500 정보기술 섹터 지수
        {'symbol': '^SP500-35', 'name': 'S&P 500 Healthcare'},  # S&P 500 헬스케어 섹터 지수
        {'symbol': '^SP500-40', 'name': 'S&P 500 Financials'},  # S&P 500 금융 섹터 지수
        # 글로벌 채권 지수
        {'symbol': 'AGG', 'name': 'Bloomberg Barclays US Aggregate Bond Index'},  # 블룸버그 바클레이즈 미국 종합 채권 지수
        {'symbol': 'BAGL', 'name': 'Bloomberg Barclays Global Aggregate Bond Index'}  # 블룸버그 바클레이즈 글로벌 종합 채권 지수
    ]
    
    for index_info in indices:
        index, created = StockIndex.objects.get_or_create(symbol=index_info['symbol'], defaults={'name': index_info['name']})
        
        try:
            # 해당 인덱스의 데이터베이스에 저장된 마지막 날짜를 가져옵니다.
            last_saved_date = HistoricalStockIndexData.objects.filter(index=index).aggregate(Max('date'))['date__max']
            
            if last_saved_date is None:
                # 데이터가 없는 경우 2010년부터 데이터 가져오기
                start_date = datetime.strptime('2010-01-01', '%Y-%m-%d')
            else:
                # 데이터가 있는 경우 마지막 저장된 날짜 이후부터 데이터 가져오기
                start_date = last_saved_date + timedelta(days=1)
            
            # 특정 인덱스의 역사적 데이터 가져오기
            index_data = fdr.DataReader(index.symbol, start=start_date.strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'))
            index_data = index_data.fillna(0, inplace=True)
            for date, data in index_data.iterrows():
                HistoricalStockIndexData.objects.update_or_create(
                    index=index,
                    date=date.date(),
                    defaults={
                        'open': data['Open'],
                        'high': data['High'],
                        'low': data['Low'],
                        'close': data['Close'],
                        'volume': data.get('Volume', None)  # 볼륨 데이터가 없는 경우도 처리
                    }
                )
            print(f"{index.symbol} 시장 인덱스 데이터 업데이트 완료")
        except Exception as e:
            print(f"Error saving historical data for {index.symbol}: {e}")

    print("주요 인덱스의 역사적 데이터 저장 완료")

def commodity_data_update():
    print("원자재 데이터를 업데이트합니다...")
    commodities = [
        {'symbol': 'GC', 'name': 'Gold'},
        {'symbol': 'SI', 'name': 'Silver'},
        {'symbol': 'CL', 'name': 'Crude Oil'},
        {'symbol': 'NG', 'name': 'Natural Gas'},
        {'symbol': 'HG', 'name': 'Copper'},
        {'symbol': 'PL', 'name': 'Platinum'},
        {'symbol': 'PA', 'name': 'Palladium'}
    ]
    
    for commodity_info in commodities:
        commodity, created = Commodity.objects.get_or_create(symbol=commodity_info['symbol'], defaults={'name': commodity_info['name']})
        
        try:
            # 해당 원자재의 데이터베이스에 저장된 마지막 날짜를 가져옵니다.
            last_saved_date = HistoricalCommodityData.objects.filter(commodity=commodity).aggregate(Max('date'))['date__max']
            
            if last_saved_date is None:
                # 데이터가 없는 경우 2010년부터 데이터 가져오기
                start_date = datetime.strptime('2010-01-01', '%Y-%m-%d')
            else:
                # 데이터가 있는 경우 마지막 저장된 날짜 이후부터 데이터 가져오기
                start_date = last_saved_date + timedelta(days=1)
            
            # 특정 원자재의 역사적 데이터 가져오기
            commodity_data = fdr.DataReader(commodity.symbol, data_source='COMMODITY', start=start_date.strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'))
            commodity_data = commodity_data.fillna(0, inplace=True)
            for date, data in commodity_data.iterrows():
                HistoricalCommodityData.objects.update_or_create(
                    commodity=commodity,
                    date=date.date(),
                    defaults={
                        'open': data['Open'],
                        'high': data['High'],
                        'low': data['Low'],
                        'close': data['Close'],
                        'volume': data.get('Volume', None)  # 볼륨 데이터가 없는 경우도 처리
                    }
                )
            print(f"{commodity.symbol} 원자재 데이터 저장 완료")
        except Exception as e:
            print(f"Error saving historical data for {commodity.symbol}: {e}")

    print("원자재의 역사적 데이터 저장 완료")