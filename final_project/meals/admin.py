from django.contrib import admin

from .models import Department, Meal, MealCategory, SpecificMeal

# Register your models here.
admin.site.register(Meal)
admin.site.register(MealCategory)
admin.site.register(Department)
admin.site.register(SpecificMeal)
