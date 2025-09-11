from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]
        widgets = {
            "text": forms.Textarea(attrs={"rows":3, "cols":60}),
            "source": forms.TextInput(attrs={"placeholder":"Фильм, книга и т.п."}),
            "weight": forms.NumberInput(attrs={"min":1}),
        }