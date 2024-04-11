from django import forms

from .models import amwell_BOA_bank_rec

class BankForm(forms.ModelForm):
    class Meta:
        model = amwell_BOA_bank_rec
        fields = ['csv_upload',]

