from django import forms
from .models import Project, ProjectImage, ProjectStep
from clients.models import Client

class ProjectForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = [
            "title",
            "client",
            "service",
            "industry",
            "duration",
            "website_url",
            "hero_image",
            "short_description",
            "overview",
            "featured",
            "status",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Project Name"
            }),

            "client": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Client Name"
            }),

            "service": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Website Development"
            }),

            "industry": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Healthcare"
            }),

            "duration": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "3 Months"
            }),

            "website_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://example.com"
            }),

            "short_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "A short summary of the project..."
            }),

            "overview": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Describe the project in detail..."
            }),

            "status": forms.Select(attrs={
                "class": "form-control"
            }),

            "featured": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "hero_image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

        }
class ProjectImageForm(forms.ModelForm):

    class Meta:

        model = ProjectImage

        fields = [

            "title",

            "description",

            "image",

            "order",

        ]


class ProjectStepForm(forms.ModelForm):

    class Meta:

        model = ProjectStep

        fields = [

            "number",

            "title",

            "description",

            "icon",

        ]        