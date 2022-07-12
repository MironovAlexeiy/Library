from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *
import datetime

class RenewBookForm(forms.ModelForm):
    # renewal_date = forms.DateField(help_text='Введите дату не более 1 месяца начиная с текущего дня', label='Дата возврата')
    class Meta:
        model = BookInstance
        fields = ['due_back']

    def clean_renewal_date(self):
        data = self.cleaned_data['due_back']
        if data < datetime.today():
            raise ValidationError("Некоректная дата")
        if data > datetime.today() + datetime.timedelta(weeks=5):
            raise ValidationError("Некоректная дата - слишком большой срок.")
        return data


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomersEditForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['number_of_passport','date_of_birthday', 'second_name', 'sex', 'ages', 'place']

# class RegistrationBook(forms.ModelForm):
#     class Meta:
#         model = Books
#         fields = '__all__'



