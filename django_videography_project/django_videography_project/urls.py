from django.contrib import admin
from django.urls import path, include
from videography import views

urlpatterns = [
    path('', views.index, name='index'),
    path('videography/', include('videography.urls')),
    path('about/', include('videography.urls'), name='about'),
    path('video/', include('videography.urls'), name='video'),
    path('admin/', admin.site.urls)
]
