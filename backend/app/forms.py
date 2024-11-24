from django import forms
from .models import JobPostingURL

class URLForm(forms.ModelForm):
    class Meta:
        model = JobPostingURL
        fields = ['url']
