from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class HomeViewTests(TestCase):
    def setUp(self):
        self.STATUS_OK = 200
        self.client = Client()
        self.home_url = reverse("home")
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            account_type="chef",
        )

    def test_GET_returns_200_response(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, self.STATUS_OK)

    def test_unauthenticated_user_sent_to_homepage(self):
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, "home.html")

    def test_authenticated_user_sent_to_portal_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse("portal"))
