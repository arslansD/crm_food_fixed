from django.urls import path

from . import views

urlpatterns = [
    path("departments/", views.DepartamentView().as_view(), name="departments"),
    path("mealCategories/", views.MealCategoryView.as_view(), name="meal-categories"),
    path("meals/", views.MealView.as_view(), name="meals"),
    path("categoriesByDepartment/<int:pk>/", views.MealCategoriesByDepartment.as_view(), name="category-by-dep"),
    path("mealsByCategory/<int:pk>", views.MealsByCategory.as_view(), name="meals-by-category")
]
