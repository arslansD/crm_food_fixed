from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models
from django.db.utils import IntegrityError

from .utils import login_creator


class Role(models.Model):
    """
    Role model. Used as a model to group user to specific group depending on their type of work
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, phone, role_id, **extra_fields):
        """
        Creates and saves a new User
        """

        if not email:
            raise ValueError("Email address is required!")

        if not first_name or not last_name:
            raise ValueError("First and Last name are required!")

        if not phone:
            raise ValueError("Phone number is required")

        if not role_id:
            raise IntegrityError("Role is required!")

        login = login_creator(last_name, first_name)

        try:
            password = extra_fields["password"]
        except KeyError:
            password = phone

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            login=login,
            phone=phone,
            role_id=role_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login, role_id, password, **extra_fields):
        """
        Creates and saves new superuser
        """
        admin_role = Role.objects.get(pk=role_id)

        user = self.model(
            email="admin",
            first_name="admin",
            last_name="admin",
            login=login,
            phone="phone",
            role_id=admin_role,
            **extra_fields
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True, blank=True)
    phone = models.CharField(max_length=255)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="workers")

    date_of_add = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ["role_id"]

    USERNAME_FIELD = 'login'

    def __str__(self):
        return f"{self.get_full_name()}, {self.phone}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

