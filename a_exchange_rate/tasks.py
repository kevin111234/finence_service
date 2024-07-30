import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

import json
from dotenv import load_dotenv
import requests
from django.utils import timezone
from a_exchange_rate.models import ExchangeRate, DollarIndex

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

def notice_message(token, channel, text, attachments):
    attachments = json.dumps(attachments)  # 리스트를 JSON으로 덤핑
    response = requests.post("https://slack.com/api/chat.postMessage",
                            headers={"Authorization": "Bearer " + token},
                            data={"channel": channel, "text": text, "attachments": attachments})

def slack_exchange():
    print("slack에 환율정보를 전송합니다")

    # 데이터베이스에서 최신 환율 정보와 달러 인덱스 정보를 가져옵니다.
    latest_exchange_rate = ExchangeRate.objects.latest('date')
    latest_dollar_index = DollarIndex.objects.latest('timestamp')

    # 알림 메시지 구성
    str1_title = f"{latest_exchange_rate.date} 현재 환율정보"
    link = 'https://kr.investing.com/currencies/us-dollar-index'
    str2_text = "환율정보 안내를 시작합니다."
    text = f'''
    환율: {latest_exchange_rate.rate}
    달러 인덱스: {latest_dollar_index.index}
    '''

    attach_dict = {
        'color': '#ff0000',
        'author_name': 'Slack Bot Notice',
        'title': str1_title,
        'title_link': link,
        'text': text
    }
    attach_list = [attach_dict]

    # 환경변수 불러오기
    load_dotenv()
    slack_token = os.getenv('API_TOKEN')

    # Slack으로 알림 전송
    notice_message(slack_token, "#주가예측-프로그램", str2_text, attach_list)
    print("Slack 알림 전송 완료")

if __name__ == '__main__':
    slack_exchange()