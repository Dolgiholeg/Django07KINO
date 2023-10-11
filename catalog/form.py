from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpform(UserCreationForm):
    username = forms.CharField(label='ЛОГИН', help_text=' ')
    password1 = forms.CharField(label='ПАРОЛЬ', help_text=' ', widget=forms.PasswordInput(attrs = {'autocomplete':'new-password'}))
    password2 = forms.CharField(label='ПОДТВЕРЖДЕНИЕ ПАРОЛЯ', help_text=' ', widget=forms.PasswordInput(attrs = {'autocomplete':'new-password'}))
    email = forms.EmailField(label='ПОЧТА',widget=forms.TextInput(attrs={'placeholder':'qwe@mail.ru'}))
    first_name = forms.CharField(label='ИМЯ', max_length=20)
    last_name = forms.CharField(label='ФАМИЛИЯ', max_length=20, required=False)



#class Meta():
    #model = User
    #fields = {'email','first_name','last_name'}
