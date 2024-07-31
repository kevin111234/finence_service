from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .models import ExchangeRate
import pandas as pd
import plotly.express as px
import plotly.io as pio
from django.core.paginator import Paginator  
from datetime import datetime, timedelta

def group_required(group_name):
    def in_group(user):
        if user.is_authenticated:
            return user.groups.filter(name=group_name).exists()
        return False
    return user_passes_test(in_group, login_url='/login/')

@group_required('exchange_rate')
def us_rate(request):
    data = ExchangeRate.objects.all().values()
    df = pd.DataFrame(data)
    page = request.GET.get('page', '1')  # 페이지
    # 날짜 형식 변환
    df['date'] = pd.to_datetime(df['date'])
    # 가장 최신 환율 데이터 가져오기
    latest_rate = ExchangeRate.objects.order_by('-date').first()
    # 환율 전체 변동 계산
    change_df = df.sort_values(by='date')  # 날짜 순서로 정렬
    change_df['rate_change'] = change_df['rate'].diff().round(3)
    change_df = change_df.iloc[::-1]
    change_df = change_df.dropna().to_dict('records')
    paginator = Paginator(change_df, 10)
    page_obj = paginator.get_page(page)
    # 그래프 생성
    three_months_ago = datetime.now() - timedelta(days=90)
    df = df[df['date'] > three_months_ago]
    df = df.sort_values(by='date')
    fig = px.line(df, x='date', y='rate', title='3개월간의 환율 변화')
    graph = pio.to_html(fig, full_html=False)
    # 컨텍스트에 데이터 추가
    context = {
        'latest_rate': latest_rate,
        'rate_changes': page_obj,
        'graph': graph,
    }
    return render(request, 'exchange_rate/us_rate.html', context)