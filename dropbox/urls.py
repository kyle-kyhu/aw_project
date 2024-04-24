from django.urls import path
from . import views

app_name = 'dropbox'

urlpatterns = [
    path('file/', views.task_file_list, name='task_file_list'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('upload/', views.upload_xfile, name='upload'),
    path('download/<int:file_id>/', views.download_xfile, name='download'),
    path('xfilelist/', views.xfilelist, name='xfilelist'),
]
