from django.test import TestCase

from users.utils import login_creator


class TestUtils(TestCase):
    """
        Class for testing utilities
    """

    def test_login_creator(self):
        """
            Testing login_creator function
        """

        first_name = "Lǎo"
        last_name = "Bǎi Xìng"

        self.assertEqual(login_creator(last_name, first_name), "Bǎi_Lǎo".lower())
