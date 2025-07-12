from django.urls import path
from . import views

urlpatterns = [
    path('', views.sleeplog_list, name='sleeplog_list'),
]
