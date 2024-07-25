from django.shortcuts import render

def home(request):
    user = request.user
    is_authenticated = user.is_authenticated
    # main groups
    is_premium= user.groups.filter(name='premium').exists() if is_authenticated else False
    is_normal= user.groups.filter(name='normal').exists() if is_authenticated else False
    #custom apps
    is_exchange_rate= user.groups.filter(name='exchange_rate').exists() if is_authenticated else False
    is_coin_analyze= user.groups.filter(name='coin_analyze').exists() if is_authenticated else False
    is_stock_analyze= user.groups.filter(name='stock_analyze').exists() if is_authenticated else False
    is_writing_ai= user.groups.filter(name='writing_ai').exists() if is_authenticated else False
    
    context = {
        'is_authenticated': is_authenticated,
        # main groups
        'is_premium': is_premium,
        'is_normal': is_normal,
        # custom apps
        'is_exchange_rate': is_exchange_rate,
        'is_coin_analyze': is_coin_analyze,
        'is_stock_analyze': is_stock_analyze,
        'is_writing_ai': is_writing_ai
    }
    return render(request, 'home.html', context)