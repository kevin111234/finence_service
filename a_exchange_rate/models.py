from django.db import models

class ExchangeRate(models.Model):
    date = models.DateField(unique=True)
    rate = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.rate}" 