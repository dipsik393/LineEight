from django import forms

from django.contrib.auth.models import User

from .models import Client


class ClientForm(forms.ModelForm):

    first_name = forms.CharField()

    last_name = forms.CharField()

    email = forms.EmailField()

    username = forms.CharField()

    password = forms.CharField(

        required=True,

        widget=forms.PasswordInput()

    )

    class Meta:

        model = Client

        fields = (

            "company",

            "phone",

            "position",

            "avatar",

            "status",

            "notes",

        )