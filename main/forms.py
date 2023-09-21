from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Exercise, UserExercise


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
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        raw_email = self.cleaned_data['email']
        if User.objects.filter(email=raw_email).exists():
            raise ValidationError("Пользователь с данным адресом электронной почты уже существует.")
        return raw_email


class EditUserExercise(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['weight'].required = False
        self.fields['distance'].required = False
        self.fields['amount'].required = False
        self.fields['time'].required = False

    class Meta:
        model = UserExercise
        fields = ('weight', 'distance', 'amount', 'time')
