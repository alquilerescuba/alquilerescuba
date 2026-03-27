from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.HiddenInput(),  # Ocultamos el campo original
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "¿Qué te pareció la propiedad? ¿Qué destacarías?",
                }
            ),
        }
        labels = {
            "comment": "Tu comentario",
        }
