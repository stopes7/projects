from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]
        labels = {
            "text": "Текст цитаты",
            "source": "Источник (фильм, книга и т.п.)",
            "weight": "Вес (чем больше, тем выше шанс появления)",
        }
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Введите цитату"
            }),
            "source": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например: Матрица, Гарри Поттер..."
            }),
            "weight": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "value": 1
            }),
        }
