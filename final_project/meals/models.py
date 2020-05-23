from django.db import models

from orders.models import Order


class Department(models.Model):
    """
        Responsible to keep Dep objects
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MealCategory(models.Model):
    """
        Responsible to keep Meal Category
    """

    name = models.CharField(max_length=50)
    department_id = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="categories"
    )

    def __str__(self):
        return self.name


class Meal(models.Model):
    """
    Responsible to keep Meal objects
    """

    name = models.CharField(max_length=50)
    category_id = models.ForeignKey(
        MealCategory, on_delete=models.CASCADE, related_name="meals"
    )
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.price} - {self.description}"


class SpecificMeal(models.Model):
    """
    Responsible to keep several meals and their price
    """
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="specific_meals")
    amount = models.IntegerField()
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="meals_id")

    def get_total_price(self):
        """
        total amount * price of the meal
        """
        total = self.meal_id.price * self.amount

        return total
