from django import forms
from .models import Blog,Subscriber


class BlogForm(forms.ModelForm):

    class Meta:

        model = Blog

        fields = [

            "title",

            "featured_image",

            "excerpt",

            "content",

            "author",

            "category",

            "reading_time",

            "meta_description",

            "featured",

            "status",

        ]

class SubscriberForm(forms.ModelForm):

    class Meta:

        model = Subscriber

        fields = ["email"]        