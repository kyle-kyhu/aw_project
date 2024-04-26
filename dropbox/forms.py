from django import forms
from .models import Dropbox

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Dropbox
        fields = ['file']

class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = Dropbox
        fields = ['excel']

                      

# class UploadXfileForm(forms.Form):
#     file = forms.FileField()

