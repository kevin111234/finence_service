from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
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
                auth_login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "Invalid username or password")
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def profile(request):
    user = request.user
    is_authenticated = user.is_authenticated
    # main groups
    is_premium= user.groups.filter(name='premium').exists() if is_authenticated else False
    is_normal= user.groups.filter(name='normal').exists() if is_authenticated else False
    context = {
        'is_authenticated': is_authenticated,
        # main groups
        'is_premium': is_premium,
        'is_normal': is_normal,
    }
    return render(request, 'user/profile.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'user/profile_update.html', {'form': form})