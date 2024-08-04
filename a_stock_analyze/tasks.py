import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

def stock_ticker_save():
    print("주식 티커 데이터 작업을 수행합니다.")
    # 주식 티커 업데이트
    from a_stock_analyze.stock_crawling import ticker_update
    ticker_update()

def stock_data_save():
    print("주식 데이터 작업을 수행합니다.")
    # 주가정보 업데이트
    from a_stock_analyze.stock_crawling import save_historical_stock_data
    save_historical_stock_data()

def stock_index_save():
    print("시장 인덱스 데이터 작업을 수행합니다.")
    # 주식 인덱스 업데이트
    from a_stock_analyze.stock_crawling import save_stockindex_data
    save_stockindex_data()

def commodity_data_save():
    print("원자재 데이터 작업을 수행합니다.")
    from a_stock_analyze.stock_crawling import save_commodity_data
    save_commodity_data()

if __name__ == '__main__':
    stock_index_save()