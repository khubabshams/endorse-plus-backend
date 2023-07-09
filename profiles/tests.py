from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

URL = '/profiles/'
ID = '1/'


class ProfileViewsTest(APITestCase):
    def setUp(self) -> None:
        """
        Create users and needed test setup data
        """
        self.AdminUser = User.objects.create_superuser(
            "adminUser", "adminuser@endorseplus.com", "pa$$wrd@7"
        )
        self.RegularUser = User.objects.create_user(
            "regularUser", "regularuser@endorseplus.com", "pa$$wrd@7"
        )

    def test_profile_exist(self) -> None:
        """
        Test created user has linked profiles
        """
        self.assertTrue(self.AdminUser.profile)
        self.assertTrue(self.RegularUser.profile)

    def test_profile_get(self) -> None:
        """
        Get profile records
        """
        list_response = self.client.get(f"{URL}")
        detail_response = self.client.get(f"{URL}{ID}")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
