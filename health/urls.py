from django.urls import path
from . import views
from . import json_upload_views

app_name = 'health'

urlpatterns = [
    path('', views.healthrecord_list, name='healthrecord_list'),
    path('add/', views.healthrecord_create, name='healthrecord_create'),
    path('<int:pk>/edit/', views.healthrecord_edit, name='healthrecord_edit'),
    path('ajax/record/<int:pk>/update/', views.healthrecord_inline_update, name='healthrecord_inline_update'),
    path('ajax/record/<int:pk>/comments/', views.healthrecord_comments, name='healthrecord_comments'),
    path('ajax/record/<int:pk>/comment/add/', views.healthrecord_comment_add, name='healthrecord_comment_add'),
    path('<int:pk>/delete/', views.healthrecord_delete, name='healthrecord_delete'),
    path('upload-json/', json_upload_views.healthrecord_upload_json, name='healthrecord_upload_json'),
    path('confirm-json/', json_upload_views.healthrecord_confirm_json, name='healthrecord_confirm_json'),
    path('bulk-rename-title/', views.bulk_rename_title, name='bulk_rename_title'),
    path('bulk-edit-by-title/', views.bulk_edit_by_title, name='bulk_edit_by_title'),
    path('symptoms/', views.symptomlog_list, name='symptomlog_list'),
    path('symptoms/add/', views.symptomlog_create, name='symptomlog_create'),
    path('symptoms/<int:pk>/delete/', views.symptomlog_delete, name='symptomlog_delete'),
    path('medications/', views.medication_list, name='medication_list'),
    path('medications/add/', views.medication_create, name='medication_create'),
    path('medications/<int:pk>/delete/', views.medication_delete, name='medication_delete'),
    path('chart-data/', views.healthrecord_chart_data, name='healthrecord_chart_data'),
    path('api/dashboard-kpi-data/', views.dashboard_kpi_data, name='dashboard_kpi_data'),
    path('api/records-by-category-data/', views.records_by_category_data, name='records_by_category_data'),
]
