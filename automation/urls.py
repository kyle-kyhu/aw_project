from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # ...
    path('', views.UploadView.as_view(), name='upload'),
    # path('review_upload/<str:file_url>/', views.ReviewUpload.as_view(), name='upload_review'),
    # ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
