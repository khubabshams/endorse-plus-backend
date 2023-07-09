import datetime
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Boost
from companies.models import Company
from experiences.models import Experience
from recommendations.models import Recommendation
from relationships.models import Relationship

URL = '/boosts/'
ID = '1/'


class BoostViewsTest(APITestCase):
    def get_boost_values(self) -> dict:
        """
        Ready to use boost data
        """
        return dict(profile=self.AdminUser.profile.id,
                    recommendation=self.Recommendation.id)

    def create_relationship(self) -> None:
        """
        Create relationship as testing data setup
        """
        self.Relationship = Relationship.objects.\
            create(name="Relationship Name")

    def create_company(self) -> None:
        """
        Create company as testing data setup
        """
        self.Company = Company.objects.create(name="Company Name")

    def create_experience(self) -> None:
        """
        Create experience as testing data setup
        """
        date = datetime.date.today()
        self.Experience = Experience.objects.\
            create(title="Experience Name",
                   profile=self.AdminUser.profile,
                   company=self.Company,
                   date_from=date,
                   is_current=True)

    def create_recommendation(self) -> None:
        """
        Create recommendation as testing data setup
        """
        self.Recommendation = Recommendation.objects.\
            create(profile=self.RegularUser.profile,
                   receiver=self.AdminUser.profile,
                   related_experience=self.Experience,
                   relation=self.Relationship,
                   content="Content")

    def create_boost(self) -> None:
        """
        Create boost as testing data setup
        """
        self.Boost = Boost.objects.create(profile=self.RegularUser.profile,
                                          recommendation=self.Recommendation)

    def create_master_data(self) -> None:
        """
        Create the testing data setup
        """
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        self.create_relationship()
        self.create_company()
        self.create_experience()
        self.client.logout()

        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        self.create_recommendation()
        self.create_boost()
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
        self.create_master_data()

    def test_boost_login_required(self) -> None:
        """
        Create boost anonymously
        """
        response = self.client.post(f"{URL}", self.get_boost_values())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_boost_no_required_fields(self) -> None:
        """
        Create boost without sending required field
        """
        values = self.get_boost_values()
        values.pop('recommendation')
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", values)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_boost_created(self) -> None:
        """
        Create boost successfully
        """
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", self.get_boost_values())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_boost_get(self) -> None:
        """
        Get boost records
        """
        list_response = self.client.get(f"{URL}")
        detail_response = self.client.get(f"{URL}{ID}")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
