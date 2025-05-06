from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/<path:data>/', views.download_qr, name='download_qr'),
]
