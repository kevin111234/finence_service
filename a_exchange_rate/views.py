from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .models import ExchangeRate
import pandas as pd
import plotly.express as px
import plotly.io as pio
from django.core.paginator import Paginator  

def group_required(group_name):
    def in_group(user):
        if user.is_authenticated:
            return user.groups.filter(name=group_name).exists()
        return False
    return user_passes_test(in_group, login_url='/login/')

@group_required('exchange_rate')
def main(request):
    # 데이터 기본 처리
    data = ExchangeRate.objects.all().values()
    df = pd.DataFrame(data)
    latest_rate = ExchangeRate.objects.order_by('-date').first() # 가장 최신 환율 데이터
    
    # 그래프 생성
    fig = px.line(df, x='date', y='rate', title='Exchange Rate Over Time')
    graph = pio.to_html(fig, full_html=False)

    context = {
        'latest_rate': latest_rate,
        'graph': graph,
        }
    
    return render(request, 'exchange_rate/main.html', context)

@group_required('exchange_rate')
def rate_detail(request):
    page = request.GET.get('page', '1')  # 페이지
    # 데이터 기본 처리
    data = ExchangeRate.objects.all().values()
    df = pd.DataFrame(data)
    exchange_rates = ExchangeRate.objects.all().order_by('-date')  # 환율 데이터를 최신 데이터부터 정렬
    # 날짜별 환율 변동 계산
    df = df.sort_values(by='date')  # 날짜 순서로 정렬
    df['rate_change'] = df['rate'].diff().round(3)
    df = df.iloc[::-1]
    df = df.dropna().to_dict('records')
    paginator = Paginator(df, 10)
    page_obj = paginator.get_page(page)

    context = {
        'exchange_rates': exchange_rates,
        'rate_changes': page_obj,
    }
    return render(request, 'exchange_rate/rate_detail.html', context)