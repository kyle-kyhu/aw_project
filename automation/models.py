from django.db import models

# Create your models here.
class amwell_BOA_bank_rec(models.Model):
    csv_upload = models.FileField(upload_to='csv/', null=True)
    excel_upload = models.FileField(upload_to='excel/', null=True)
    date = models.DateField()

    def __str__(self):
        return self.date
    