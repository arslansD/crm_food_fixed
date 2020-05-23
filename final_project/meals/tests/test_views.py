from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from meals import serializers
from meals.models import Department, Meal, MealCategory
from .utils import DepartmentFactory, MealCategoryFactory, MealFactory, fake

DEPARTMENT_URL = reverse("departments")
MEAL_CATEGORY_URL = reverse("meal-categories")
MEALS_URL = reverse("meals")


class TestDepartmentView(TestCase):
    """
        Testing endpoints for Departments model
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_departments(self):
        """
        Testing GET method for department model, expecting list of departments
        """
        DepartmentFactory()
        DepartmentFactory()

        response = self.client.get(DEPARTMENT_URL)

        departments = Department.objects.all()
        serializer = serializers.DepartmentSerializer(departments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_create_department(self):
        """
        Testing POST method on departments/ endpoint with some data
        """
        payload = {
            "name": "Keke"
        }

        response = self.client.post(DEPARTMENT_URL, payload, format="json")
        exists = Department.objects.filter(name=payload["name"]).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)


class TestMealCategoryView(TestCase):
    """
    Class for testing endpoints of MealCategory model
    """

    def setUp(self) -> None:
        self.department = DepartmentFactory()
        self.client = APIClient()

    def test_list_categories(self):
        """
        Testing GET method for MealCategory model, expecting list of categories
        """
        MealCategoryFactory()
        MealCategoryFactory()

        response = self.client.get(MEAL_CATEGORY_URL)

        categories = MealCategory.objects.all()
        serializer = serializers.MealCategorySerializer(categories, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(categories, [])
        self.assertEqual(serializer.data, response.data)

    def test_create_category(self):
        """
        Testing creation of MealCategory object through API
        """
        payload = {
            "name": "Kitchen",
            "department_id": self.department.id,
        }

        response = self.client.post(MEAL_CATEGORY_URL, payload, format="json")
        exists = MealCategory.objects.filter(name=payload["name"]).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_custom_delete_method(self):
        """
        Testing custom handling of DELETE method
        """
        category = MealCategoryFactory()
        payload = {
            "id": category.id
        }

        response = self.client.delete(MEAL_CATEGORY_URL, payload, format="json")
        exists = MealCategory.objects.filter(id=payload["id"]).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)


class TestMealsViews(TestCase):
    """
    Class for testing endpoints of Meal model
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_meals_list(self):
        """
        Testing GET method on meals/ endpoint
        """

        MealFactory()
        MealFactory()

        response = self.client.get(MEALS_URL)

        meals = Meal.objects.all()
        serializer = serializers.MealSerializer(meals, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(meals, [])
        self.assertEqual(serializer.data, response.data)

    def test_post_meal(self):
        """
        Testing creation of Meal object through API
        """
        category = MealCategoryFactory()

        payload = {
            "name": "Ash",
            "category_id": category.id,
            "description": fake.paragraph(nb_sentences=3),
            "price": fake.pyint(min_value=120, max_value=9999)
        }

        response = self.client.post(MEALS_URL, data=payload, format="json")
        exists = Meal.objects.filter(name=payload["name"]).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_custom_delete(self):
        """
        Testing custom handling of DELETE method
        """

        meal = MealFactory()
        payload = {
            "id": meal.id
        }

        response = self.client.delete(MEALS_URL, payload)
        exists = MealCategory.objects.filter(id=payload["id"]).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)

    def test_custom_patch(self):
        """
        Testing partial update through PATCH method
        """
        meal = MealFactory()

        payload = {
            "id": meal.id,
            "name": "lagman",
            "price": 123
        }

        response = self.client.patch(MEALS_URL, data=payload, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["name"], payload["name"])
        self.assertEqual(response_data["price"], payload["price"])

    def test_custom_put(self):
        """
        Testing full update through PUT method
        """
        meal = MealFactory()
        category = MealCategoryFactory()
        payload = {
            "id": meal.id,
            "name": "lagman",
            "price": 123,
            "category_id": category.id,
            "description": "Kekek"
        }

        response = self.client.put(MEALS_URL, data=payload, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["name"], payload["name"])
        self.assertEqual(response_data["price"], payload["price"])
        self.assertEqual(response_data["category_id"], payload["category_id"])
        self.assertEqual(response_data["description"], payload["description"])


class TestOtherViews(TestCase):
    """
    Testing other views, which belongs to meals
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_categories_by_dep(self):
        """
        Testing class, which should return list of categories belonging to specific model
        """
        department1 = DepartmentFactory()
        department2 = DepartmentFactory()

        category1 = MealCategoryFactory(department_id=department1)
        MealCategoryFactory(department_id=department2)

        response = self.client.get(reverse("meals"), args=[category1.id])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
