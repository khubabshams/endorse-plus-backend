import datetime
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Experience
from companies.models import Company

URL = '/experiences/'
ID = '1/'


class ExperienceViewsTest(APITestCase):
    def get_experience_values(self) -> dict:
        """
        Ready to use experience data
        """
        return dict(title="Experience Name",
                    profile=self.RegularUser.profile.id,
                    company=self.Company.id,
                    date_from=self.Date,
                    is_current=True)

    def create_company(self) -> None:
        """
        Create company as testing data setup
        """
        self.Company = Company.objects.create(name="Company Name")

    def create_experience(self) -> None:
        """
        Create experience as testing data setup
        """
        self.Date = datetime.date.today()
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        self.create_company()
        Experience.objects.create(title="Experience Name",
                                  profile=self.RegularUser.profile,
                                  company=self.Company,
                                  date_from=self.Date,
                                  is_current=True)
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
        self.create_experience()

    def test_experience_login_required(self) -> None:
        """
        Create experience anonymously
        """
        response = self.client.post(f"{URL}", self.get_experience_values())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_experience_no_required_fields(self) -> None:
        """
        Create experience without sending required field
        """
        values = self.get_experience_values()
        values.pop('title')
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", values)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_experience_created(self) -> None:
        """
        Create experience successfully
        """
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", self.get_experience_values())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_experience_get(self) -> None:
        """
        Get experience records
        """
        list_response = self.client.get(f"{URL}")
        detail_response = self.client.get(f"{URL}{ID}")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
