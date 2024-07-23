from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import datetime

class CustomUserCreationForm(UserCreationForm):
    year = forms.ChoiceField(
        choices=[(year, year) for year in range(1900, datetime.datetime.now().year + 1)],
        required=True,
        label="Year"
    )
    month = forms.ChoiceField(
        choices=[(month, month) for month in range(1, 13)],
        required=True,
        label="Month"
    )
    day = forms.ChoiceField(
        choices=[(day, day) for day in range(1, 32)],
        required=True,
        label="Day"
    )
    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'username', 'email', 'date_of_birth', 'gender', 'password1', 'password2')
        
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
        self.fields['date_of_birth'].label = '생년월일 6자리'
    
    def clean_date_of_birth(self):
        year = int(self.cleaned_data.get('year'))
        month = int(self.cleaned_data.get('month'))
        day = int(self.cleaned_data.get('day'))

        try:
            date_of_birth = datetime.date(year, month, day)
        except ValueError:
            raise ValidationError("Invalid date.")
        
        if date_of_birth > datetime.date.today():
            raise ValidationError("The date of birth cannot be in the future.")
        
        return date_of_birth
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.date_of_birth = self.clean_date_of_birth()
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    year = forms.ChoiceField(
        choices=[(year, year) for year in range(1900, datetime.datetime.now().year + 1)],
        required=True,
        label="Year"
    )
    month = forms.ChoiceField(
        choices=[(month, month) for month in range(1, 13)],
        required=True,
        label="Month"
    )
    day = forms.ChoiceField(
        choices=[(day, day) for day in range(1, 32)],
        required=True,
        label="Day"
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'gender')
    
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
        self.fields['date_of_birth'].label = '생년월일 6자리'
    
    def clean_date_of_birth(self):
        year = int(self.cleaned_data.get('year'))
        month = int(self.cleaned_data.get('month'))
        day = int(self.cleaned_data.get('day'))

        try:
            date_of_birth = datetime.date(year, month, day)
        except ValueError:
            raise ValidationError("Invalid date.")
        
        if date_of_birth > datetime.date.today():
            raise ValidationError("The date of birth cannot be in the future.")
        
        return date_of_birth

    def save(self, commit=True):
        user = super().save(commit=False)
        user.date_of_birth = self.clean_date_of_birth()
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='유저 ID', max_length=30, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)