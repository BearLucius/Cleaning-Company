from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from .models import Request, Service
from django.contrib.auth import authenticate
class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'

class UserRegistrationForm(StyleFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')
    FIO = forms.CharField(
        max_length=50,
        label='ФИО',
        validators=[
            MaxLengthValidator(50, message="ФИО не должно превышать 50 символов."),
            RegexValidator(
                regex=r'^[a-zA-Zа-яА-ЯёЁ\s]+$',
                message="ФИО должно содержать только буквы и пробелы."
            )
        ]
    )
    phone_regex = RegexValidator(
        regex=r'^[0-9\+]+$',
        message="Телефон должен содержать только  цифры и символ +"
    )
    phone = forms.CharField(
        validators=[phone_regex, MaxLengthValidator(11)],
        max_length=11,
        label='Телефон'
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'confirm_password', 'FIO', 'phone', 'email']
        labels = {
            'username': 'Логин',
            'email': 'Email',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data


class UserLoginForm(StyleFormMixin, forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Пытаемся аутентифицировать пользователя
        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError("Пользователь с таким логином или паролем не существует.")

        return cleaned_data

class RequestForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Request
        fields = ['address', 'contact_info', 'service', 'preferred_date_time', 'payment_type']
        widgets = {
            'preferred_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'address': 'Адрес',
            'contact_info': 'Контактная информация',
            'service': 'Услуга',
            'preferred_date_time': 'Дата и время',
            'payment_type': 'Тип оплаты',
        }
