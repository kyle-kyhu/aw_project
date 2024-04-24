from django import forms
from .models import Dropbox

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Dropbox
        fields = ['file']

class UploadXfileForm(forms.Form):
    file = forms.FileField()

