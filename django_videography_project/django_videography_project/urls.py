from django.contrib import admin
from django.urls import path, include
from videography import views

urlpatterns = [
    path('', views.index, name='index'),
    path('videography/', include('videography.urls')),
    path('about/', include('videography.urls')),
    path('video/', include('videography.urls')),
    path('admin/', admin.site.urls)

]
