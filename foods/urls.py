from django.urls import path
from .views import FoodItemListView, AdminFoodItemView, CategoryListView, AdminCategoryView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('admin/categories/', AdminCategoryView.as_view(),
         name='admin-category-create'),
    path('admin/categories/<int:pk>/', AdminCategoryView.as_view(),
         name='admin-category-update'),
    path('', FoodItemListView.as_view(), name='food-list'),
    path('admin/items/', AdminFoodItemView.as_view(), name='admin-food-create'),
    path('admin/items/<int:pk>/', AdminFoodItemView.as_view(),
         name='admin-food-update'),
]
