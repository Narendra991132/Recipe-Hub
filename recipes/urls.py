from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Recipe CRUD
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/create/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:pk>/update/', views.recipe_update, name='recipe_update'),
    path('recipes/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),  # New URL for user's recipes
    
    # Category CRUD
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]