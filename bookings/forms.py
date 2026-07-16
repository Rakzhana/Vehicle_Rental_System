from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            "pickup_date",
            "return_date",
        ]

        widgets = {
            "pickup_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "return_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }


class ReviewForm(forms.ModelForm):

    RATING_CHOICES = [
        (1, "⭐ 1 - Poor"),
        (2, "⭐⭐ 2 - Fair"),
        (3, "⭐⭐⭐ 3 - Good"),
        (4, "⭐⭐⭐⭐ 4 - Very Good"),
        (5, "⭐⭐⭐⭐⭐ 5 - Excellent"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Write your review here...",
            }
        )
    )

    class Meta:
        model = Booking
        fields = [
            "rating",
            "review",
        ]