from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Relationship

URL = '/relationships/'
ID = '1/'


class RelationshipViewsTest(APITestCase):
    def create_relationship(self) -> None:
        """
        Create relationship as testing data setup
        """
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        Relationship.objects.create(name="Relationship Name")
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
        self.create_relationship()

    def test_relationship_login_required(self) -> None:
        """
        Create relationship anonymously
        """
        response = self.client.post(f"{URL}", {"name": "Relationship Name"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_relationship_admin_login_required(self) -> None:
        """
        Create relationship with regular user login
        """
        self.client.login(username=self.RegularUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", {"name": "Relationship Name"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_relationship_no_required_fields(self) -> None:
        """
        Create relationship without sending required field
        """
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(
            f"{URL}", {"description": "Relationship Description"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_relationship_created(self) -> None:
        """
        Create relationship successfully
        """
        self.client.login(username=self.AdminUser.username,
                          password="pa$$wrd@7")
        response = self.client.post(f"{URL}", {"name": "Relationship Name"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_relationship_get(self) -> None:
        """
        Get relationship records
        """
        list_response = self.client.get(f"{URL}")
        detail_response = self.client.get(f"{URL}{ID}")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
