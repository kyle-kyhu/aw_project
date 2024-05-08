from django.urls import path
from .views import (
    TaskFileListView,
    FileDetailView,
    RunScriptView,
    DownloadView,
)

app_name = 'dropbox'

urlpatterns = [
    # testing this url logic 
    path('file/', TaskFileListView.as_view(), name='task_file_list'),
    path('file/detail/', FileDetailView.as_view(), name='file_detail'),
    path('file/detail/run/', RunScriptView.as_view(), name='run_script'),
    path('file/detail/download/', DownloadView.as_view(), name='download'),
]

'''urls for classes with <int:file_id> set up'''
# path('file/', TaskFileListView.as_view(), name='task_file_list'),
    # path('file/<int:file_id>/', FileDetailView.as_view(), name='file_detail'),
    # path('file/<int:file_id>/run/', RunScriptView.as_view(), name='run_script'),
    # path('file/<int:file_id>/download/', DownloadView.as_view(), name='download'),


'''urls for functions'''
    # path('file/', views.task_file_list, name='task_file_list'),
    # path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    # path('file/<int:file_id>/run/', views.run_script, name='run_script'),
    # path('file/<int:file_id>/download/', views.download, name='download'),