from django.urls import path
from . import views

app_name = 'dropbox'

urlpatterns = [
    path('file/', views.task_file_list, name='task_file_list'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('file/<int:file_id>/run/', views.run_script, name='run_script'),
    # path('success/', views.success_view, name='success'),
    path('file/<int:file_id>/download/', views.download, name='download'),
    # path('upload/', views.upload_xfile, name='upload'), #cagdas
    # path('download/<int:file_id>/', views.download_xfile, name='download'),
    # path('xfilelist/', views.xfilelist, name='xfilelist'),
]
