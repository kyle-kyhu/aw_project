from django.contrib import admin

from .models import Dropbox, PyScript, Task_file, xfile

class DropboxAdmin(admin.ModelAdmin):
    list_display = (
        'file', 
        'created_at',
        'excel',
        )
    list_filter = ('created_at',)


class PyScriptAdmin(admin.ModelAdmin):
    list_display = ('py_file', 'py_name') 
            

class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('task_name',)

class xFileAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Dropbox, DropboxAdmin)
admin.site.register(xfile, xFileAdmin)
admin.site.register(PyScript, PyScriptAdmin)
admin.site.register(Task_file, TaskFileAdmin)
