from django.urls import path, include
from . import views

app_name = 'exchange_rate'

urlpatterns = [
    path('', views.us_rate, name='us_rate'),
]