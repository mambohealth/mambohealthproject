from django.urls import path
from . import views

urlpatterns = [
    path('', views.nutritionlog_list, name='nutritionlog_list'),
    path('confirm/', views.nutritionlog_confirm, name='nutritionlog_confirm'),
    path('save/', views.save_nutrition_log, name='save_nutrition_log'),
    path('edit/<int:log_id>/', views.edit_nutrition_log, name='edit_nutrition_log'),
    path('delete/<int:log_id>/', views.delete_nutrition_log, name='delete_nutrition_log'),
    path('update_name/', views.update_nutrition_name, name='update_nutrition_name'),
    path('foods/', views.food_list, name='food_list'),
    path('foods/create/', views.create_food, name='create_food'),
    path('foods/edit/<int:food_id>/', views.edit_food, name='edit_food'),
    path('foods/delete/<int:food_id>/', views.delete_food, name='delete_food'),
]
