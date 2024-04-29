from django.db import models


class Dropbox(models.Model):
    file = models.FileField(upload_to='files/')
    excel = models.FileField(upload_to='files/', null=True)
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.excel:  # Ensure 'excel' is present before using its name
            self.name = self.excel.name
        else:
            self.name = self.file.name  # Fall back to the CSV name if no Excel
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    
    
class xfile(models.Model):
    name = models.CharField(max_length=255)
    data = models.BinaryField()

    def __str__(self):
        return self.name

class PyScript(models.Model):
    py_file = models.FileField(upload_to='py_file')
    py_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.py_name

class Task_file(models.Model):
    task_name = models.CharField(max_length=100, blank=True)

    def __str_(self):
        return self.task_name
               