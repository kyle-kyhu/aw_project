from django.contrib import admin

from .models import Dropbox, PyScript, Task_file

class DropboxAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_at')
    list_filter = ('created_at',)


class PyScriptAdmin(admin.ModelAdmin):
    list_display = ('py_file', 'py_name') 
            

class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('task_name',)


admin.site.register(Dropbox, DropboxAdmin)
admin.site.register(PyScript, PyScriptAdmin)
admin.site.register(Task_file, TaskFileAdmin)
