import datetime
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Recommendation
from companies.models import Company
from experiences.models import Experience
from relationships.models import Relationship

URL = '/recommendations/'
ID = '1/'


class RecommendationViewsTest(APITestCase):
    def get_recommendation_values(self) -> dict:
        """
        Ready to use recommendation data
        """
        return dict(profile=self.RegularUser.profile.id,
                    receiver=self.AdminUser.profile.id,
                    related_experience=self.Experience.id,
                    relation=self.Relationship.id,
                    content="Content")

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

    def create_recommendation(self) -> None:
        """
        Create recommendation as testing data setup
        """
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        Recommendation.objects.\
            create(profile=self.RegularUser.profile,
                   receiver=self.AdminUser.profile,
                   related_experience=self.Experience,
                   relation=self.Relationship,
                   content="Content")
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

    def test_recommendation_login_required(self) -> None:
        """
        Create recommendation anonymously
        """
        response = self.client.post(f"{URL}", self.get_recommendation_values())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recommendation_no_required_fields(self) -> None:
        """
        Create recommendation without sending required field
        """
        values = self.get_recommendation_values()
        values.pop('receiver')
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", values)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recommendation_created(self) -> None:
        """
        Create recommendation successfully
        """
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", self.get_recommendation_values())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_recommendation_get(self) -> None:
        """
        Get recommendation records
        """
        self.create_recommendation()
        list_response = self.client.get(f"{URL}")
        detail_response = self.client.get(f"{URL}{ID}")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
