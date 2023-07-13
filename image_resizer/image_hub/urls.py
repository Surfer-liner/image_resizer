from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'image_hub'

urlpatterns = [
    path('', views.ResizePictureView.as_view(), name='resize_picture'),
    path('resized_images/<str:filename>/', views.resized_image_view, name='resized_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
