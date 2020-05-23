import datetime

from django.test import TestCase

from users.models import User
from users.serializers import RoleSerializer as RS, UserCreateSerializer as UCR, \
    UserDetailSerializer as UDS
from .utils import RoleFactory, fake


class TestSerializers(TestCase):
    """
        Class for testing user and role serializers\
    """

    def setUp(self):
        self.role = RoleFactory()

    def test_role_serializer(self):
        """
            Testing role serializer
        """

        role = {
            "name": "Staff member"
        }
        serializer = RS(data=role)
        valid = serializer.is_valid()

        self.assertTrue(valid)

    def test_user_create_serializer(self):
        """
            Testing user serializer
        """

        user = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "role_id": self.role.id,
        }

        serializer = UCR(data=user)
        valid = serializer.is_valid()
        self.assertTrue(valid)

    def test_create_method_on_serializer(self):
        """
            Testing create method in UserCreateSerializer
        """

        user = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "role_id": self.role.id,
        }
        serializer = UCR(data=user)
        serializer.is_valid()
        serializer.save()

        exists = User.objects.filter(
            email=user["email"],
            phone=user["phone"]
        ).exists()
        self.assertTrue(exists)

    def test_user_detail_serializer(self):
        """
            Testing UserDetailSerializer serializer
        """
        user_data = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "role_id": self.role.id,
            "password": "!@#$%^78",
            "date_of_add": datetime.datetime.now(),
            "login": "1231",
        }
        serializer = UDS(data=user_data)
        valid = serializer.is_valid()
        self.assertTrue(valid)
