from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from meals.tests.utils import MealFactory, SMFactory
from orders import models, serializers
from .utils import OrderFactory, TableFactory, create_user_model, ServiceFactory

TABLES_URL = reverse("tables")
ORDERS_URL = reverse("orders")
CHECKS_URL = reverse("checks")
MEALS_TO_ORDERS = reverse("meals-to-orders")


class TestTableViews(TestCase):
    """
    Testing table views
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_tables(self):
        """
        Testing GET method for table view
        """

        TableFactory()
        TableFactory()
        tables = models.Table.objects.all()

        response = self.client.get(TABLES_URL)
        serializer = serializers.TableSerializer(tables, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_table(self):
        """
        Testing POST method for table view
        """
        payload = {
            "name": "Table#1"
        }

        response = self.client.post(TABLES_URL, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_table(self):
        """
        Testing DELETE method for table view
        """
        table = TableFactory()

        payload = {
            "id": table.id
        }

        response = self.client.delete(TABLES_URL, data=payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderViews(TestCase):
    """
    Testing order views
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_orders(self):
        """
        Testing GET method of order view
        """
        user = create_user_model()

        OrderFactory(waiter_id=user)
        OrderFactory(waiter_id=user)

        orders = models.Order.objects.all()
        serializer = serializers.OrderSerializer(orders, many=True)

        response = self.client.get(ORDERS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_post_order(self):
        """
        Testing POST method of order view
        """
        user = create_user_model()
        table = TableFactory()
        meal = MealFactory()
        meal2 = MealFactory()

        self.client.force_authenticate(user)

        payload = {
            "table_id": table.id,
            'meals_id': [
                {
                    "meal_id": meal.id,
                    "amount": 4
                },
                {
                    "meal_id": meal2.id,
                    "amount": 6
                }
            ]
        }

        response = self.client.post(ORDERS_URL, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_order(self):
        """
        Testing DELETE method of order view
        """

        order = OrderFactory()

        payload = {
            "id": order.id
        }

        response = self.client.delete(ORDERS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_add_meal_to_order(self):
    #     """
    #     Testing adding meal to order
    #     """
    #     user = create_user_model()
    #     order = OrderFactory(waiter_id=user)
    #     meal = MealFactory()
    #     SMFactory(order_id=order)
    #
    #     payload = {
    #         "order_id": order.id,
    #         "meals_id": [
    #             {
    #                 "meal_id": meal.id,
    #                 "amount": 123
    #             }
    #         ]
    #     }
    #
    #     response = self.client.post(MEALS_TO_ORDERS, data=payload)
    #
    #     print(response.data)
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(meal.amount, 8)


class TestCheckView(TestCase):
    """
    Testing Check views
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_all_checks(self):
        """
        Testing GET method for CheckView
        """

        user = create_user_model()
        order = OrderFactory(waiter_id=user)
        order2 = OrderFactory(waiter_id=user)

        SMFactory(order_id=order)
        SMFactory(order_id=order2)

        models.Check.objects.create_check(order_id=order)
        models.Check.objects.create_check(order_id=order2)

        response = self.client.get(CHECKS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_check(self):
        """
        Testing POST method for CheckView
        """

        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        SMFactory(order_id=order)

        payload = {
            "order_id": order.id
        }

        response = self.client.post(CHECKS_URL, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_check(self):
        """
        Testing DELETE method for CheckView
        """
        user = create_user_model()
        self.client.force_authenticate(user)
        order = OrderFactory(waiter_id=user)

        SMFactory(order_id=order)

        check = models.Check.objects.create_check(order_id=order)

        payload = {
            "id": check.id
        }

        response = self.client.delete(CHECKS_URL, data=payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestStatusViews(TestCase):
    """
    Class for testing Status and Service percentage views
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_statuses(self):
        """
        Testing GET method for statuses view
        """

        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        models.Status(order_id=order, name="Completed")

        response = self.client.get(reverse('statuses', args=[order.id]))

        serializer = serializers.StatusesOfOrder(order)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_status(self):
        """
        Testing POST method for statuses view
        """

        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        self.client.force_authenticate(user)

        payload = {
            "name": "Completed"
        }

        response = self.client.post(reverse('statuses', args=[order.id]), data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_status(self):
        """
        Testing DELETE method for statuses view
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        stat = models.Status.objects.create(order_id=order, name="Completed")

        payload = {
            "id": stat.id
        }

        self.client.force_authenticate(user)

        response = self.client.delete(reverse('statuses', args=[order.id]), data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPercentageViews(TestCase):
    """
    Testing Percentage view
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_service_percentage(self):
        """
        Testing GET Method for service view
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        percentage = ServiceFactory(order_id=order)

        response = self.client.get(reverse('percentage', args=[percentage.order_id.id]))

        serializer = serializers.SpSerializer(percentage)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_service_percentage(self):
        """
        Testing POST Method for service percentage view
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        payload = {
            "order_id": order.id,
            "percentage": 13123
        }

        response = self.client.post(reverse('create_percentage'), data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_percentage(self):
        """
        Testing DELETE Method for service percentage ciew
        """
        user = create_user_model()
        order = OrderFactory(waiter_id=user)

        percentage = ServiceFactory(order_id=order)

        response = self.client.delete(reverse('percentage', args=[percentage.order_id.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
