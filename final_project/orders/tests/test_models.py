from django.db.utils import IntegrityError
from django.test import TestCase

from meals.tests.utils import SMFactory
from orders import models
from .utils import OrderFactory, TableFactory, create_user_model, ServiceFactory


class TestModels(TestCase):
    """
    Testing meals and related models
    """

    def test_tables(self):
        """
        Testing creation of Table model
        """
        name = "Any Table"
        table = TableFactory(name=name)

        self.assertEqual(str(table), name)

    def test_orders(self):
        """
        Testing creation of Order model
        """
        table = TableFactory()
        user = create_user_model()

        order = models.Order.objects.create(waiter_id=user, table_id=table)

        self.assertEqual(str(order), f"Order #{order.id}, {order.date}")

    def test_orders_with_specific_meals(self):
        """
        Testing creation of order model with specific meals
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        special_meal1 = SMFactory(order_id=order)
        special_meal2 = SMFactory(order_id=order)

        related_meals = order.meals_id.all()
        self.assertIn(special_meal1, related_meals)
        self.assertIn(special_meal2, related_meals)

    def test_order_without_user(self):
        """
        Testing creation of order without User model
        """
        user = None

        with self.assertRaises(IntegrityError):
            OrderFactory(waiter_id=user)

    def test_order_without_table(self):
        """
        Testing creation of order without Table model
        """
        table = None

        with self.assertRaises(IntegrityError):
            OrderFactory(table_id=table)

    def test_create_status(self):
        """
        Testing creation of status
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        status = models.Status(order_id=order, name="to do")

        self.assertEqual(str(status), f"{status.order_id}-{status.name}")

    def test_create_service_percentage(self):
        """
        Testing creation of service percentage
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        percentage = ServiceFactory(order_id=order, percentage=34)

        self.assertEqual(str(percentage), f"{str(order)}- {34}%")


class TestCheckModel(TestCase):
    """
    Testing check model
    """

    def test_check_model_creation(self):
        """
        Testing creation of check model
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        check = models.Check.objects.create(order_id=order, service_fee=123, total_sum=1234)

        self.assertEqual(str(check), f"Order ID-{check.order_id.id}, Date-{check.date}, Total sum-{check.total_sum}")

    def test_create_check(self):
        """
        Testing custom create check method Of CheckManager
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        s_meal = SMFactory(order_id=order)
        s_meal2 = SMFactory(order_id=order)

        total_sum = s_meal.get_total_price() + s_meal2.get_total_price()

        check = models.Check.objects.create_check(order_id=order)

        self.assertEqual(check.total_sum, total_sum)
        self.assertEqual(check.service_fee, total_sum / 4)
        self.assertEqual(order.is_open, False)
