from django.urls import path, include
from . import views

app_name = 'exchange_rate'

urlpatterns = [
    path('', views.main, name='main'),
]