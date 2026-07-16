from django import forms
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email"
        ]