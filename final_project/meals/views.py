from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from core.mixins import CustomDeleteMixin, CustomUpdateMixin
from . import serializers
from .models import Department, Meal, MealCategory


class DepartamentView(ListCreateAPIView, CustomDeleteMixin):
    """
    Responsible for endpoints/views of departments model
    """

    queryset = Department.objects.all()
    model = Department
    serializer_class = serializers.DepartmentSerializer

    def delete(self, request, *args, **kwargs):
        """
        Needed  for "DELETE" method, which accepts the id from request and delete corresponding model
        """
        return self.destroy(request, *args, **kwargs)


class MealCategoryView(ListCreateAPIView, CustomDeleteMixin):
    """
    Responsible for endpoints/views of MealCategory model
    """
    model = MealCategory
    queryset = MealCategory.objects.all()
    serializer_class = serializers.MealCategorySerializer

    def delete(self, request, *args, **kwargs):
        """
        Needed  for "DELETE" method, which accepts the id from request and delete corresponding model
        """
        return self.destroy(request, *args, **kwargs)


class MealView(ListCreateAPIView, CustomDeleteMixin, CustomUpdateMixin):
    """
    Responsible for endpoints/views of Meals model
    """
    model = Meal
    queryset = Meal.objects.all()
    serializer_class = serializers.MealSerializer

    def delete(self, request, *args, **kwargs):
        """
        Needed  for "DELETE" method, which accepts the id from request and delete corresponding model
        """
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class MealCategoriesByDepartment(RetrieveAPIView):
    """
    Responsible for serving list of categories, which belong to specific department
    """

    model = Department
    queryset = Department.objects.all()
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        categories = MealCategory.objects.filter(department_id=instance.id)
        serializer = serializers.MealCategorySerializer(categories, many=True)
        return Response(serializer.data)


class MealsByCategory(RetrieveAPIView):
    """
    Responsible for serving list of meals, which belong to specific category
    """

    model = MealCategory
    queryset = MealCategory.objects.all()
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        meals = Meal.objects.filter(category_id=instance.id)
        serializer = serializers.MealSerializer(meals, many=True)
        return Response(serializer.data)

