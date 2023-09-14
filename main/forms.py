from django import forms
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
