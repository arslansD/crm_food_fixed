import factory
from faker import Faker

from users import models

fake = Faker()


class RoleFactory(factory.django.DjangoModelFactory):
    """
        Class for creating random role models
    """

    class Meta:
        model = models.Role

    name = fake.job()


def get_fake_user_data(role):
    return {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number(),
        "role_id": role,
    }
