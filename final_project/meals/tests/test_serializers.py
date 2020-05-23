from django.test import TestCase

from meals import serializers
from .utils import DepartmentFactory, MealCategoryFactory, fake


class TestSerializers(TestCase):
    """
    Testing serializers for Meal, MealCategory, and Department models
    """

    def test_department_serializer(self):
        """
        Testing Department serializer for validity against some data
        """
        payload = {
            "name": "Kitchen"
        }

        serializer = serializers.DepartmentSerializer(data=payload)
        valid = serializer.is_valid()
        self.assertTrue(valid)

    def test_meal_category_serializer(self):
        """
        Testing MealCategory serializer for validity against some data
        """
        department = DepartmentFactory()
        payload = {
            "name": "Salads",
            "department_id": department.id
        }

        serializer = serializers.MealCategorySerializer(data=payload)
        valid = serializer.is_valid()
        self.assertTrue(valid)

    def test_meal_serializer(self):
        """
        Testing Meal serializer for validity against some data
        """
        meal_category = MealCategoryFactory()
        payload = {
            "name": fake.word(ext_word_list=None),
            "category_id": meal_category.id,
            "price": fake.pyint(),
            "description": fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)
        }

        serializer = serializers.MealSerializer(data=payload)
        valid = serializer.is_valid()
        self.assertTrue(valid)
