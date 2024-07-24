from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'username', 'email', 'gender', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        # 표시되는 이름 변경
        self.fields['username'].label = '유저 ID'
        self.fields['first_name'].label = '이름'
        self.fields['last_name'].label = '성'
        self.fields['email'].label = '이메일 주소'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'gender')

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '유저 ID'
        self.fields['email'].label = '이메일 주소'
        self.fields['first_name'].label = '이름'
        self.fields['last_name'].label = '성'

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='유저 ID', max_length=30, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)
