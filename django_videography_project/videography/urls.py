from django.urls import path
from videography import views

app_name = 'videography'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('video/<str:pk>/', views.video, name='video'),
    path('collection/', views.collection, name='collection'),
    path('feedback/', views.feedback, name='feedback'),
]