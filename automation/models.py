from django.db import models

# Create your models here.
class amwell_BOA_bank_rec(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=100)
    