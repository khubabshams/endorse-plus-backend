from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Request
from companies.models import Company

URL = '/requests/'
ID = '1/'


class RequestViewsTest(APITestCase):
    def get_request_values(self) -> dict:
        """
        Ready to use request data
        """
        return dict(profile=self.RegularUser.profile.id,
                    receiver=self.AdminUser.profile.id,
                    message="Message")

    def create_request(self) -> None:
        """
        Create request as testing data setup
        """
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        Request.objects.create(profile=self.RegularUser.profile,
                               receiver=self.AdminUser.profile,
                               message="Message")
        self.client.logout()

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
        self.create_request()

    def test_request_login_required(self) -> None:
        """
        Create request anonymously
        """
        response = self.client.post(f"{URL}", self.get_request_values())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_no_required_fields(self) -> None:
        """
        Create request without sending required field
        """
        values = self.get_request_values()
        values.pop('receiver')
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", values)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_created(self) -> None:
        """
        Create request successfully
        """
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", self.get_request_values())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_get(self) -> None:
        """
        Get request records
        """
        list_response = self.client.get(f"{URL}")
        detail_response = self.client.get(f"{URL}{ID}")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
