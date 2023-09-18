from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Exercise


class AddExercise(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('name', 'category', 'media', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'name'}),
            'description': forms.Textarea(attrs={'class': 'description'}),
        }
        labels = {
            'name': 'Название',
            'category': 'Категория',
            'media': 'Демонстрация',
            'description': 'Описание',
        }

    def clean_name(self):
        raw_name = self.cleaned_data['name']
        raw_name = raw_name[0].lower() + raw_name[1:]
        return raw_name


class CreateUser(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтвердите пароль'

        self.fields['password1'].help_text = 'Минимум 8 символов, не может состоять только из цифр'
        self.fields['password2'].help_text = 'Введите пароль еще раз для подтверждения'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
        help_texts = {
            'username': 'Обязательное поле. Максимум 150 символов. Только буквы, цифры и @/./+/-/_',
        }
