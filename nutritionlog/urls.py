from django.urls import path
from . import views

urlpatterns = [
    path('', views.nutritionlog_list, name='nutritionlog_list'),
]
