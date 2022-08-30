from django.contrib.auth.models import User

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


from django.urls.base import reverse

# Create your tests here.


class TestSchoolView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()

    def test_create_and_fetch_school(self):
        payload = {
            "email": "test@test.com",
            "name": "New School",
            "city": "East",
            "pincode": "123456",
            "password": "aaa",
            "username": "admin7",
        }
        create_url = reverse("create_school")
        resp = self.api_client.post(create_url, payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)

        # Test auth and fetch
        user_id = resp.data["user"]
        user = User.objects.get(id=user_id)
        token = RefreshToken.for_user(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        fetch_id = resp.data["id"]
        fetch_url = reverse("retrieve_school", kwargs={"pk": fetch_id})
        resp = self.api_client.get(fetch_url, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
