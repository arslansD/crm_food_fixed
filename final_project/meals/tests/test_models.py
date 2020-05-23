from django.db.utils import IntegrityError
from django.test import TestCase

from .utils import DepartmentFactory, MealCategoryFactory, MealFactory, fake


class TestModels(TestCase):
    """
        Class for testing meals and related models
    """

    def test_department(self):
        """
            Testing creation of Departments model
        """
        name = "Kitchen"
        department = DepartmentFactory(
            name=name
        )

        self.assertEqual(str(department), name)

    def test_meal_category_without_department(self):
        """
            Testing meal category without department
        """
        department = None

        with self.assertRaises(IntegrityError):
            MealCategoryFactory(department_id=department)

    def test_meal_category(self):
        """
            Testing creation of Meal Category model
        """

        name = "Drink"
        department = DepartmentFactory()
        category = MealCategoryFactory(
            name=name,
            department_id=department
        )

        self.assertEqual(str(category), name)
        self.assertEqual(category.department_id, department)

    def test_meals_without_category(self):
        """
            Testing meal without meal category model
        """
        category = None

        with self.assertRaises(IntegrityError):
            MealFactory(category_id=category)

    def test_meals(self):
        """
            Testing creation of Meals model
        """

        name = "Salads"
        price = fake.pyint()
        description = fake.paragraph(nb_sentences=3)
        category = MealCategoryFactory()

        meal = MealFactory(
            name=name,
            description=description,
            price=price,
            category_id=category,
        )

        self.assertEqual(str(meal), f"{name} - {price} - {description}")
        self.assertEqual(meal.category_id, category)
