from .models import Project, Rate
from django import forms

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'date_added']


class RateProjectForm(forms.ModelForm):
    class Meta:
        model = Rate
        exclude = ['owner', 'project']