from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def group_required(group_name):
    def in_group(user):
        if user.is_authenticated:
            return user.groups.filter(name=group_name).exists()
        return False
    return user_passes_test(in_group, login_url='/login/')

@group_required('exchange_rate')
def main(request):
    return render(request, 'exchange_rate/main.html')