from django.urls import path, include
from . import views

app_name = 'exchange_rate'

urlpatterns = [
    path('', views.main, name='main'),
    path('rate_detail', views.rate_detail, name='rate_detail')
]