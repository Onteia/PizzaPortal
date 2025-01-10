from django.test import TestCase, Client
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth import get_user_model
from ..models import Pizza, Topping


class PortalViewTests(TestCase):
    def setUp(self):
        self.STATUS_OK = 200
        self.client = Client()
        self.portal_url = reverse("portal")
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            account_type="owner",
        )

    def test_unauthenticated_redirected_to_login(self):
        response = self.client.get(self.portal_url)
        self.assertRedirects(response, reverse("login"))
        response = self.client.post(self.portal_url)
        self.assertRedirects(response, reverse("login"))

    def test_authenticated_user_returns_200_response(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.portal_url)

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "portal.html")


class AddViewTests(TestCase):
    def setUp(self):
        self.STATUS_OK = 200
        self.client = Client()
        self.add_url = reverse("add")
        self.owner_user = get_user_model().objects.create_user(
            username="test_owner",
            password="test_password",
            account_type="owner",
        )
        self.chef_user = get_user_model().objects.create_user(
            username="test_chef",
            password="test_password",
            account_type="chef",
        )

    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(self.add_url)
        self.assertRedirects(response, reverse("login"))
        response = self.client.post(self.add_url)
        self.assertRedirects(response, reverse("login"))

    def test_chef_GET_returns_200_response(self):
        self.client.force_login(self.chef_user)
        response = self.client.get(self.add_url)

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "add.html")

    def test_owner_GET_returns_200_response(self):
        self.client.force_login(self.owner_user)
        response = self.client.get(self.add_url)

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "add.html")

    def test_valid_chef_POST_redirected_to_portal(self):
        self.client.force_login(self.chef_user)
        topping = Topping.objects.create(name="Cheese")
        data = {
            "name": "Cheese Pizza",
            "description": "Regular cheese pizza.",
            "cost": 9.99,
            "toppings": [topping.id],
        }
        response = self.client.post(self.add_url, data=data)

        self.assertRedirects(response, reverse("portal"))

    def test_valid_owner_POST_redirected_to_portal(self):
        self.client.force_login(self.owner_user)
        data = {
            "name": "Muenster Cheese",
        }
        response = self.client.post(self.add_url, data=data)

        self.assertRedirects(response, reverse("portal"))

    def test_invalid_chef_POST_returns_200(self):
        self.client.force_login(self.chef_user)
        response = self.client.post(self.add_url, data={})

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "add.html")

    def test_invalid_owner_POST_returns_200(self):
        self.client.force_login(self.owner_user)
        response = self.client.post(self.add_url, data={})

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "add.html")


class EditViewTests(TestCase):
    def setUp(self):
        self.STATUS_OK = 200
        self.client = Client()
        self.owner_user = get_user_model().objects.create_user(
            username="test_owner",
            password="test_password",
            account_type="owner",
        )
        self.chef_user = get_user_model().objects.create_user(
            username="test_chef",
            password="test_password",
            account_type="chef",
        )
        self.topping = Topping.objects.create(name="Cheese")
        self.pizza = Pizza.objects.create(name="Cheese Pizza", cost=9.99)
        self.pizza.toppings.add(self.topping)

    def test_unauthenticated_user_redirected_to_login(self):
        url = reverse("edit", kwargs={"item_id": self.pizza.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login"))
        response = self.client.post(url)
        self.assertRedirects(response, reverse("login"))

    def test_no_item_id_raises_no_reverse_match(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse("edit"))

    def test_chef_GET_returns_200_response(self):
        self.client.force_login(self.chef_user)
        url = reverse("edit", kwargs={"item_id": self.pizza.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "edit.html")

    def test_owner_GET_returns_200_response(self):
        self.client.force_login(self.owner_user)
        url = reverse("edit", kwargs={"item_id": self.topping.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "edit.html")

    def test_valid_chef_POST_redirected_to_portal(self):
        self.client.force_login(self.chef_user)
        data = {
            "name": self.pizza.name,
            "description": "New Description",
            "cost": self.pizza.cost,
            "toppings": self.pizza.toppings.in_bulk(),
        }
        url = reverse("edit", kwargs={"item_id": self.pizza.id})
        response = self.client.post(url, data=data)

        self.assertRedirects(response, reverse("portal"))

    def test_valid_owner_POST_redirected_to_portal(self):
        self.client.force_login(self.owner_user)
        data = {
            "name": self.topping.name,
            "additional_cost": 0.99,
        }
        url = reverse("edit", kwargs={"item_id": self.topping.id})
        response = self.client.post(url, data=data)

        self.assertRedirects(response, reverse("portal"))

    def test_invalid_chef_POST_returns_200(self):
        self.client.force_login(self.chef_user)
        url = reverse("edit", kwargs={"item_id": self.pizza.id})
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "edit.html")

    def test_invalid_owner_POST_returns_200(self):
        self.client.force_login(self.owner_user)
        url = reverse("edit", kwargs={"item_id": self.topping.id})
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertTemplateUsed(response, "edit.html")

    def test_invalid_pizza_id_raises_no_reverse_match(self):
        self.client.force_login(self.chef_user)

        with self.assertRaises(NoReverseMatch):
            reverse("edit", kwargs={"item_id": -1})

    def test_invalid_topping_id_raises_no_reverse_match(self):
        self.client.force_login(self.owner_user)

        with self.assertRaises(NoReverseMatch):
            reverse("edit", kwargs={"item_id": -1})


class DeleteViewTests(TestCase):
    def setUp(self):
        self.STATUS_OK = 200
        self.client = Client()
        self.owner_user = get_user_model().objects.create_user(
            username="test_owner",
            password="test_password",
            account_type="owner",
        )
        self.chef_user = get_user_model().objects.create_user(
            username="test_chef",
            password="test_password",
            account_type="chef",
        )

    def test_unauthenticated_user_redirected_to_login(self):
        pizza = Pizza.objects.create(name="Sample pizza name", cost=12.99)
        url = reverse("delete", kwargs={"item_id": pizza.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login"))
        response = self.client.post(url)
        self.assertRedirects(response, reverse("login"))

    def test_no_item_id_raises_no_reverse_match(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse("delete"))

    def test_chef_GET_redirected_to_portal(self):
        self.client.force_login(self.chef_user)
        pizza = Pizza.objects.create(name="Sample pizza name", cost=12.99)
        url = reverse("delete", kwargs={"item_id": pizza.id})
        response = self.client.get(url)

        self.assertRedirects(response, reverse("portal"))

    def test_owner_GET_redirected_to_portal(self):
        self.client.force_login(self.owner_user)
        pizza = Pizza.objects.create(name="Sample pizza name", cost=12.99)
        url = reverse("delete", kwargs={"item_id": pizza.id})
        response = self.client.get(url)

        self.assertRedirects(response, reverse("portal"))

    def test_chef_POST_redirected_to_portal(self):
        self.client.force_login(self.chef_user)
        pizza = Pizza.objects.create(name="Temporary Pizza", cost=2.99)
        url = reverse("delete", kwargs={"item_id": pizza.id})
        response = self.client.post(url)

        self.assertRedirects(response, reverse("portal"))

    def test_owner_POST_redirected_to_portal(self):
        self.client.force_login(self.owner_user)
        topping = Topping.objects.create(name="Sample topping name")
        url = reverse("delete", kwargs={"item_id": topping.id})
        response = self.client.post(url)

        self.assertRedirects(response, reverse("portal"))

    def test_invalid_pizza_id_raises_no_reverse_match(self):
        self.client.force_login(self.chef_user)

        with self.assertRaises(NoReverseMatch):
            reverse("delete", kwargs={"item_id": -1})

    def test_invalid_topping_id_raises_no_reverse_match(self):
        self.client.force_login(self.owner_user)

        with self.assertRaises(NoReverseMatch):
            reverse("delete", kwargs={"item_id": -1})
