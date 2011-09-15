from django import forms

class DeploymentForm(forms.Form):
    action  = forms.CharField(required=True, max_length=50)
    commit  = forms.CharField(required=True, max_length=50)
