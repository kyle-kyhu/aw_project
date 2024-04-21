from django.db import models

# Create your models here.
class Dropbox(models.Model):
    file = models.FileField(upload_to='files/')
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PyScript(models.Model):
    py_file = models.FileField(upload_to='py_file')
    py_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.py_name
