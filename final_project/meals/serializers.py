from rest_framework import serializers

from .models import Department, Meal, MealCategory, SpecificMeal


class DepartmentSerializer(serializers.ModelSerializer):
    """
        Responsible for serializing Department
    """

    class Meta:
        model = Department
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("id",)


class MealCategorySerializer(serializers.ModelSerializer):
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )

    class Meta:
        model = MealCategory
        fields = (
            "id",
            "name",
            "department_id",
        )
        read_only_fields = ("id",)


class MealSerializer(serializers.ModelSerializer):
    """
    Responsible for serializing Meals
    """
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=MealCategory.objects.all()
    )

    class Meta:
        model = Meal
        fields = (
            "id",
            "category_id",
            "name",
            "price",
            "description"
        )
        read_only_fields = ("id",)


class CategoriesByDep(serializers.ModelSerializer):
    """
    Class for serializing categories by their department
    """
    categories = MealCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = (
            "categories",
        )


class SmSerializer(serializers.ModelSerializer):
    """
    Responsible for serializing specific meals and their amount
    """
    meal_id = serializers.PrimaryKeyRelatedField(
        queryset=Meal.objects.all()
    )

    class Meta:
        model = SpecificMeal
        fields = (
            "meal_id",
            "amount",
        )
