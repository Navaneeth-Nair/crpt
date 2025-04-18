from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_page),  # ← serves upload.html
    path('push/', views.push),
    path('pull/', views.pull),
    path('branches/<str:repo_name>/', views.branches),
]
