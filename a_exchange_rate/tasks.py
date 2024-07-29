def crawling_exchange():
    print("환율정보 크롤링 작업을 수행합니다.")
# 환율정보 크롤링
    import exchange_rate_crawling
    crawler = exchange_rate_crawling.ExchangeRateCrawler()
    crawler.run()
# 달러인덱스 크롤링
    print("달러인덱스 크롤링 작업을 수행합니다.")

def slack_exchange():
    print("slack에 환율정보를 전송합니다")
    # 환율, 달러인덱스 전송