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
    print("달러인덱스 크롤링 작업을 수행합니다.")

def slack_exchange():
    print("slack에 환율정보를 전송합니다")
    # 환율, 달러인덱스 전송

if __name__ == '__main__':
    crawling_exchange()