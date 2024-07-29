import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

class ExchangeRateCrawler: # 데이터 구성용 class
    def __init__(self): #class 정의 시 바로 실행
        self.base_url = 'https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW&page='
        self.date_list = []
        self.rate_list = []

    def generate_urls(self, pages): # url 구성
        return [f'{self.base_url}{i+1}' for i in range(pages)]
    
    def crawl_data(self, urls): # 크롤링 진행
        for url in tqdm(urls, desc="크롤링 진행도", unit="page"):
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            for row in soup.find_all("tr"):
                cells_date = row.find_all("td", class_="date")
                cells_num = row.find_all("td", class_="num")
                if cells_date and cells_num:
                    date_text = cells_date[0].text.strip()
                    rate_text = cells_num[0].text.strip().replace(",", "")
                    self.date_list.append(date_text)
                    self.rate_list.append(float(rate_text))

    def create_dataframe(self): # 데이터프레임으로 변환
        return pd.DataFrame({
            "날짜": self.date_list,
            "환율": self.rate_list
        })

    def save_to_database(self, df): # 데이터베이스에 저장
        print("데이터베이스에 저장합니다...")

    def run(self): # 함수 실행문
        urls = self.generate_urls(37)
        self.crawl_data(urls)
        df = self.create_dataframe()
        print(df, "다음 내용을 데이터베이스에 저장합니다...")
        self.save_to_database(df)
        print("데이터베이스에 저장 완료!")
