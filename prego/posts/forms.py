from django import forms

from .models import PostTranslation


class PostTranslationForm(forms.ModelForm):
    class Meta:
        model = PostTranslation
        fields = ["post", "title", "body", "language", "draft"]
