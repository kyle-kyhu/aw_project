from django.urls import path
from . import views

app_name = 'dropbox'

urlpatterns = [
    path('file/', views.file_list, name='file_list'),
    path('file_detail/<int:file_id>/', views.file_detail, name='file_detail'),
]
