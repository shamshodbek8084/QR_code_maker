from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/<str:data>/', views.download_qr, name='download_qr'),
]
