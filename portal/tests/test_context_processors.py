from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Topping


class ContextProcessorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")
        self.portal_url = reverse("portal")
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password", account_type="owner"
        )
        Topping.objects.create(name="sample_topping")

    def test_unauthenticated_user_has_no_context(self):
        response = self.client.get(self.home_url)
        context = response.context
        self.assertNotIn("acct_type", context)
        self.assertNotIn("items", context)

    def test_authenticated_user_has_context(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.portal_url)
        topping = Topping.objects.all()
        self.assertEquals(response.context["acct_type"], "Owner")
        self.assertQuerySetEqual(response.context["items"], topping)
