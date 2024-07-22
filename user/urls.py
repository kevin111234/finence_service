from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
]