from django import forms
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):

    class Meta:

        model = SiteSettings

        fields = "__all__"