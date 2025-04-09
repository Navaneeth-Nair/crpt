from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('remote.urls')),  # 👈 include your remote app's URLs
]

