from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user:profile')
            else:
                form.add_error(None, "Invalid username or password")
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    return render(request, 'user/profile.html')