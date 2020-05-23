from django.test import TestCase

from . import utils


class TestRoleModel(TestCase):
    """
        Testing publicly available endpoints for user app
    """

    def test_roles_model(self):
        """
            Testing Role model creation
        """

        role_name = "Waiter"
        role = utils.RoleFactory(name=role_name)
        self.assertEqual(str(role), role_name)
