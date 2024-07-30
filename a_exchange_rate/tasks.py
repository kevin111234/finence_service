import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def crawling_exchange():
# 환율정보 크롤링
    print("환율정보 크롤링 작업을 수행합니다.")
    from a_exchange_rate.exchange_rate_crawling import ExchangeRateCrawler  # 절대 경로 사용
    crawler = ExchangeRateCrawler()
    crawler.run()
# 달러인덱스 크롤링

def crawling_index():
    from a_exchange_rate.exchange_rate_crawling import DollarIndexCrawler
    from datetime import datetime
    from a_exchange_rate.models import DollarIndex
    # DollarIndexCrawler를 사용하여 달러 인덱스를 가져옵니다.
    Index = DollarIndexCrawler()
    # 현재 시간을 가져옵니다.
    now = datetime.now()

    # 데이터베이스에 달러 인덱스와 현재 시간을 저장합니다.
    dollar_index, created = DollarIndex.objects.get_or_create(
        timestamp=now,
        defaults={'index': Index}
    )
    if not created:
        dollar_index.index = Index
        dollar_index.save()

    print(f"달러 인덱스 저장 완료: {Index} at {now}")


def slack_exchange():
    print("slack에 환율정보를 전송합니다")
    # 환율, 달러인덱스 전송

if __name__ == '__main__':
    crawling_index()