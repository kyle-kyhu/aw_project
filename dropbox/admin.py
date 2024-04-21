from django.contrib import admin

from .models import Dropbox, PyScript

class DropboxAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_at')
    list_filter = ('created_at',)


class PyScriptAdmin(admin.ModelAdmin):
    list_display = ('py_file', 'name') 
            



admin.site.register(Dropbox)
admin.site.register(PyScript)
