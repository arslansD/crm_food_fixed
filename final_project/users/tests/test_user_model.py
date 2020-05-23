from django.db.utils import IntegrityError
from django.test import TestCase

from users.models import User
from users.utils import login_creator
from .utils import RoleFactory, fake


class TestUserModel(TestCase):
    """
    Testing publicly available endpoints for user app
    """

    def setUp(self):
        """
        Initial setUp for all tests
        """
        self.role = RoleFactory()
        self.user_data = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "role_id": self.role,
        }

    def test_create_user_without_role(self):
        """
        Testing that user can't be created without role model
        """

        role = None
        self.user_data["role_id"] = role

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)

    def test_create_user_without_first_name(self):
        """
        Testing that user model can't be created without first name
        """

        first_name = ""
        self.user_data["first_name"] = first_name

        with self.assertRaises(ValueError):
            User.objects.create_user(**self.user_data)

    def test_create_user_without_last_name(self):
        """
        Testing that user model can't be created without last name
        """

        last_name = ""
        self.user_data["last_name"] = last_name

        with self.assertRaises(ValueError):
            User.objects.create_user(**self.user_data)

    def test_create_user_without_phone_number(self):
        """
        Testing that user model can't be created without phone number
        """

        phone = ""
        self.user_data["phone"] = phone

        with self.assertRaises(ValueError):
            User.objects.create_user(**self.user_data)

    def test_create_user_without_email(self):
        email = ""
        self.user_data["email"] = email

        with self.assertRaises(ValueError):
            User.objects.create_user(**self.user_data)

    def test_create_user_model(self):
        """
        Testing creation of user model
        """

        role = self.role
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(role, user.role_id)
        self.assertEqual(str(user), f"{user.first_name} {user.last_name}, {user.phone}")
        self.assertTrue(user.check_password(user.phone))

    def test_user_login(self):
        """
        Testing user login field
        """

        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.login, login_creator(user.last_name, user.first_name))

    def test_create_super_user(self):
        """
        Testing creation of super user
        """

        user = User.objects.create_superuser("admin", self.role.id, "admin")

        self.assertTrue(user.is_superuser)
