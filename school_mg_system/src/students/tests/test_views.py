from django.contrib.auth.models import User
from django.test import TestCase
from django.urls.base import reverse
from rest_framework.test import APIClient

from src.schools.models import School

# Create your tests here.


class StudentViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(
            username="SchoolAdmin", password="schoolpass", is_staff=True
        )
        cls.school = School.objects.create(
            user=cls.user, name="School", city="Imphal", pincode="603203"
        )

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.school.user)

    def test_create_and_fetch_student(self):
        payload = {"name": "Stud3", "password": "1234", "username": "Stud3"}
        create_url = reverse("student")
        resp = self.client.post(create_url, payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)

        resp = self.client.get(create_url, payload, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_update_student(self):
        payload = {"name": "Stud3", "password": "1234", "username": "Stud3"}
        create_url = reverse("student")
        resp = self.client.post(create_url, payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)

        student_id = resp.data["id"]
        patch_url = reverse("update_student", kwargs={"pk": student_id})
        patch_payload = {
            "name": "Stud4",
            "password": "1243",
        }
        resp = self.client.patch(patch_url, patch_payload, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_bulk_create(self):
        payload = [
            {"name": f"Student{i}", "password": "1234", "username": f"StudentNew{i}"}
            for i in range(0, 20)
        ]
        create_url = "%s?grade=%s" % (reverse("add_bulk_students"), 8)
        resp = self.client.post(create_url, payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertEqual(len(resp.data), 20)
