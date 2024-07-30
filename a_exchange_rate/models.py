from django.db import models

class ExchangeRate(models.Model):
    date = models.DateField(unique=True)
    rate = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.rate}" 
    
class DollarIndex(models.Model):
    index = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.index} at {self.timestamp}"