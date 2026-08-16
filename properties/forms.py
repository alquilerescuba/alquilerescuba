from django import forms
from .models import Review, Property  # ← AÑADE 'Property' a la importación


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.HiddenInput(),
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


# ============================================
# NUEVO FORMULARIO PARA PROPIEDADES
# ============================================
class PropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Si el usuario no es staff, ocultamos el campo is_featured
        if self.user and not self.user.is_staff:
            self.fields.pop("is_featured", None)

    class Meta:
        model = Property
        exclude = ["owner", "created_at", "updated_at", "average_rating"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "address": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "guests": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "bathrooms": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "rental_type": forms.Select(attrs={"class": "form-select"}),
            "price_category": forms.Select(attrs={"class": "form-select"}),
            "price_per_night": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "price_per_month": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "price_per_daypass": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "main_photo": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "has_stable_electricity": "⚡ Corriente eléctrica estable (respaldo)",
        }
