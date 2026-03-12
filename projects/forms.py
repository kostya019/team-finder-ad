from django import forms

from .models import Project
from .validators import validate_github_repo_url


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status",]

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        if github_url:
            validated_url = validate_github_repo_url(github_url)
            return validated_url
        return github_url

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'github_url' in self.cleaned_data:
            instance.github_url = self.cleaned_data['github_url']
        if commit:
            instance.save()
        return instance
