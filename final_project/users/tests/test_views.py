from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users import serializers
from users.models import Role, User
from .utils import RoleFactory, fake, get_fake_user_data

ROLES_URL = reverse("roles")

USERS_URL = reverse("users")


class TestRoleView(TestCase):
    """
    Testing Role model endpoints
    """

    def setUp(self) -> None:
        """
        Initial setUp for all tests
        """
        self.client = APIClient()

    def test_list_view(self):
        """
        Testing listing of role models
        """
        RoleFactory()
        RoleFactory()

        response = self.client.get(ROLES_URL)

        roles = Role.objects.all()
        serializer = serializers.RoleSerializer(roles, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_role(self):
        """
        Testing creation of role model
        """

        payload = {
            "name": "Waiter"
        }

        response = self.client.post(ROLES_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        exists = Role.objects.filter(name=response.data["name"]).exists()
        self.assertTrue(exists)

    def test_delete_role(self):
        """
        Testing deletion of role model
        """
        role = RoleFactory(name="Admin")

        payload = {
            'id': role.id
        }

        response = self.client.delete(ROLES_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestUserEndpoints(TestCase):
    """
    Testing user endpoints
    """

    def setUp(self) -> None:
        """
        Initial setUp for all tests
        """
        self.role = RoleFactory()
        self.user_data = get_fake_user_data(self.role)
        self.client = APIClient()

        user = User.objects.create_user(**get_fake_user_data(self.role))
        self.client.force_authenticate(user)

    def test_get_all_users(self):
        """
        Testing on GET method on users/ endpoint, should return list of users
        """
        User.objects.create_user(**self.user_data)
        user_data = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "role_id": self.role,
        }
        User.objects.create_user(**user_data)

        response = self.client.get(USERS_URL)
        users = User.objects.all()
        serializer = serializers.UserDetailSerializer(users, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_user_endpoint(self):
        """
        Testing user creation on users/ endpoint
        """
        self.user_data["role_id"] = self.role.id
        response = self.client.post(USERS_URL, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        exists = User.objects.filter(email=response.data["email"]).exists()
        self.assertTrue(exists)

    def test_user_delete_endpoint(self):
        """
        Testing custom delete method on users/ endpoint
        """
        user = User.objects.create_user(**self.user_data)

        payload = {
            'id': user.pk
        }

        response = self.client.delete(USERS_URL, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_user_update(self):
        """
        Testing custom PATCH method on users/ endpoint
        """
        user = User.objects.create_user(**self.user_data)
        payload = {
            "id": user.id,
            "first_name": "Aika",
            "last_name": "Ivanova",
            "password": "Some cool pass",
            "email": "sample@example.com",
            "phone": "0771234123"
        }

        response = self.client.patch(USERS_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data

        self.assertEqual(response_data["first_name"], payload["first_name"])
        self.assertEqual(response_data["last_name"], payload["last_name"])
        self.assertEqual(response_data["email"], payload["email"])
        self.assertEqual(response_data["phone"], payload["phone"])

    def test_put_user_update(self):
        """
        Testing custom PUT method on users/ endpoint
        """
        role = RoleFactory()
        user = User.objects.create_user(**self.user_data)
        payload = {
            "id": user.id,
            "first_name": "Aika",
            "last_name": "Ivanova",
            "password": "Some cool pass",
            "email": "sample@example.com",
            "role_id": role.id,
            "phone": "0771234123"
        }

        response = self.client.put(USERS_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data

        self.assertEqual(response_data["first_name"], payload["first_name"])
        self.assertEqual(response_data["last_name"], payload["last_name"])
        self.assertEqual(response_data["email"], payload["email"])
        self.assertEqual(response_data["phone"], payload["phone"])
        self.assertEqual(response_data["role_id"], payload["role_id"])

    def test_user_registration(self):
        """
        Testing User registration
        """
        self.user_data["role_id"] = self.role.id
        response = self.client.post(reverse("register"), self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("token", response.data)

    def test_user_login(self):
        """
        Testing User login and token
        """
        self.client.logout()

        user = User.objects.create_user(**self.user_data)
        payload = {
            "login": user.login,
            "password": user.phone
        }
        response = self.client.post(reverse("token_obtain_pair"), data=payload)

        self.assertIn("access", response.data)

        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response2 = self.client.get(reverse("users"))

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
