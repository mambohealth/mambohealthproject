from django.urls import path
from . import views
from . import json_upload_views

app_name = 'health'

urlpatterns = [
    path('', views.healthrecord_list, name='healthrecord_list'),
    path('add/', views.healthrecord_create, name='healthrecord_create'),
    path('<int:pk>/edit/', views.healthrecord_edit, name='healthrecord_edit'),
    path('<int:pk>/delete/', views.healthrecord_delete, name='healthrecord_delete'),
    path('upload-json/', json_upload_views.healthrecord_upload_json, name='healthrecord_upload_json'),
    path('confirm-json/', json_upload_views.healthrecord_confirm_json, name='healthrecord_confirm_json'),
    path('bulk-rename-title/', views.bulk_rename_title, name='bulk_rename_title'),
    path('bulk-edit-by-title/', views.bulk_edit_by_title, name='bulk_edit_by_title'),
]
