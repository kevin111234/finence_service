import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawling_exchange():
    print("환율정보 크롤링 작업을 수행합니다.")
    # 환율정보 크롤링
    # 달러인덱스 크롤링
    base_url = 'https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW&page='
    date_list = []
    rate_list = []
    for i in range(37):
        url = f'{base_url}{i+1}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        for row in soup.find_all("tr"):
            cells_date = row.find_all("td", class_="date")
            cells_num = row.find_all("td", class_="num")
            if cells_date and cells_num:
                date_text = cells_date[0].text.strip()
                rate_text = cells_num[0].text.strip().replace(",", "")
                date_list.append(date_text)
                rate_list.append(float(rate_text))
    df = pd.DataFrame({"날짜": date_list, "환율": rate_list})
    print(df, "다음 내용을 데이터베이스에 저장합니다...")

def slack_exchange():
    print("slack에 환율정보를 전송합니다")
    # 환율, 달러인덱스 전송