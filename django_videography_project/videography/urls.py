from django.urls import path
from videography import views

app_name = 'videography'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]