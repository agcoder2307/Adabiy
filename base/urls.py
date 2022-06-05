from . import views
from django.urls import path

urlpatterns = [
    path('check/', views.CheckText, name='check-text'),
    path('punctuation/', views.CheckPunctuation, name='check-punctuation'),
]
