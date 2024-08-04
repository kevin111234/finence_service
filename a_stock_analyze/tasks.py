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

def crawling_statement():
    print("재무제표 작업을 수행합니다.")
    # 분기별/ 월별로 수행
    # 재무제표 업데이트

if __name__ == '__main__':
    stock_data_save()