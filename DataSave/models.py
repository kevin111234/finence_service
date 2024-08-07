from django.db import models

# 주식 정보
class Stock(models.Model): # 주식 티커 테이블
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    industry_code = models.CharField(max_length=20)
    industry = models.CharField(max_length=100)
    exchange = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

class HistoricalStockData(models.Model): # 주가정보 테이블
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('stock', 'date')

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"

class StockIndex(models.Model): # 시장 지표 티커 테이블
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

class HistoricalStockIndexData(models.Model): # 시장 지표 테이블
    index = models.ForeignKey(StockIndex, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('index', 'date')

    def __str__(self):
        return f"{self.index.symbol} - {self.date}"
    
class Commodity(models.Model): # 원자재 티커 테이블
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

class HistoricalCommodityData(models.Model): # 원자재 데이터 테이블
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('commodity', 'date')

    def __str__(self):
        return f"{self.commodity.symbol} - {self.date}"
    

# 환율 정보