from django.urls import path
from . import views

app_name = 'fileapp'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('download/', views.download, name='download'),
]
