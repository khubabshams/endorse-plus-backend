from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Company

URL = '/companies/'
ID = '1/'


class CompanyViewsTest(APITestCase):
    def create_company(self) -> None:
        """
        Create company as testing data setup
        """
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        Company.objects.create(name="Company Name")
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
        self.create_company()

    def test_company_login_required(self) -> None:
        """
        Create company anonymously
        """
        response = self.client.post(f"{URL}", {"name": "Company Name"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_admin_login_required(self) -> None:
        """
        Create company with regular user login
        """
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", {"name": "Company Name"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_no_required_fields(self) -> None:
        """
        Create company without sending required field
        """
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(
            f"{URL}", {"description": "Company Description"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_company_created(self) -> None:
        """
        Create company successfully
        """
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", {"name": "Company Name"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_company_get(self) -> None:
        """
        Get company records
        """
        list_response = self.client.get(f"{URL}")
        detail_response = self.client.get(f"{URL}{ID}")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
