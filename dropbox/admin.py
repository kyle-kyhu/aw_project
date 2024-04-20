from django.contrib import admin

from .models import Dropbox

class DropboxAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_at')
    list_filter = ('created_at',)



admin.site.register(Dropbox)
