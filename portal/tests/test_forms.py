from django.test import TestCase
from django.http import HttpRequest
from ..forms import PizzaForm, ToppingForm
from ..models import Topping


class PizzaFormTests(TestCase):
    def setUp(self):
        self.topping_instance = Topping.objects.create(name="Cheese")
        self.request = HttpRequest()

    def test_empty_form_contains_all_fields(self):
        form = PizzaForm()

        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("cost", form.fields)
        self.assertIn("toppings", form.fields)

    def test_empty_name_raises_value_error(self):
        self.request.POST = {
            "description": "Some description",
            "cost": 12.99,
            "toppings": [self.topping_instance.id],
        }
        form = PizzaForm(self.request.POST)

        with self.assertRaises(ValueError):
            form.save()

    def test_empty_description_is_valid(self):
        self.request.POST = {
            "name": "Some name",
            "cost": 12.99,
            "toppings": [self.topping_instance.id],
        }
        form = PizzaForm(self.request.POST)

        self.assertTrue(form.is_valid())

    def test_empty_cost_raises_value_error(self):
        self.request.POST = {
            "name": "Some name",
            "description": "Some description",
            "toppings": [self.topping_instance.id],
        }
        form = PizzaForm(self.request.POST)

        with self.assertRaises(ValueError):
            form.save()

    def test_duplicate_name_raises_value_error(self):
        duplicate_name = "Same name"
        unique_topping = Topping.objects.create(name="New Topping")
        self.request.POST = {
            "name": duplicate_name,
            "cost": 12.99,
            "toppings": [self.topping_instance.id],
        }
        form = PizzaForm(self.request.POST)
        form.save()
        self.request.POST = {
            "name": duplicate_name,
            "description": "Different description",
            "cost": 10.99,
            "toppings": [unique_topping.id],
        }
        form = PizzaForm(self.request.POST)

        with self.assertRaises(ValueError):
            form.save()

    def test_duplicate_topping_raises_value_error(self):
        duplicate_toppings = [self.topping_instance.id]
        self.request.POST = {
            "name": "Unique name",
            "cost": 12.99,
            "toppings": duplicate_toppings,
        }
        form = PizzaForm(self.request.POST)
        form.save()
        self.request.POST = {
            "name": "Different name",
            "cost": 15.99,
            "toppings": duplicate_toppings,
        }
        form = PizzaForm(self.request.POST)

        with self.assertRaises(ValueError):
            form.save()

    def test_creating_valid_pizza_results_in_valid_form(self):
        cheese_topping = self.topping_instance
        pepperoni_topping = Topping.objects.create(name="Pepperoni")
        self.request.POST = {
            "name": "Cheese Pizza",
            "description": "Have you ever wanted a tasty pizza?",
            "cost": 9.99,
            "toppings": [cheese_topping.id],
        }
        first_form = PizzaForm(self.request.POST)
        self.request.POST = {
            "name": "Pepperoni Pizza",
            "cost": 9.99,
            "toppings": [cheese_topping.id, pepperoni_topping.id],
        }
        second_form = PizzaForm(self.request.POST)

        self.assertTrue(first_form.is_valid())
        self.assertTrue(second_form.is_valid())

    def test_no_available_toppings_raises_value_error(self):
        Topping.objects.get(name=self.topping_instance.name).delete()
        self.request.POST = {
            "name": "Some name",
            "description": "Some description",
            "cost": 12.99,
            "toppings": [],
        }
        form = PizzaForm(self.request.POST)
        Topping.objects.create(name=self.topping_instance.name)

        with self.assertRaises(ValueError):
            form.save()

    def test_changing_instance_name_modifies_name(self):
        self.request.POST = {
            "name": "Cheese Pizza",
            "cost": 12.99,
            "toppings": [self.topping_instance],
        }
        form = PizzaForm(self.request.POST)
        form.save()
        self.request.POST = {
            "name": "New York Style Cheese Pizza",
            "cost": form.instance.cost,
            "toppings": form.instance.toppings.all(),
        }
        form = PizzaForm(self.request.POST, instance=form.instance)
        form.save()

        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.name, "New York Style Cheese Pizza")

    def test_changing_instance_description_modifies_description(self):
        self.request.POST = {
            "name": "Cheese Pizza",
            "description": "Just a regular cheese pizza.",
            "cost": 12.99,
            "toppings": [self.topping_instance],
        }
        form = PizzaForm(self.request.POST)
        form.save()
        self.request.POST = {
            "name": form.instance.name,
            "description": "Our world-famous cheese pizza made with real mozzarella cheese!",
            "cost": form.instance.cost,
            "toppings": form.instance.toppings.all(),
        }
        form = PizzaForm(self.request.POST, instance=form.instance)
        form.save()

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.instance.description,
            "Our world-famous cheese pizza made with real mozzarella cheese!",
        )

    def test_changing_instance_cost_modifies_cost(self):
        self.request.POST = {
            "name": "Cheese Pizza",
            "cost": 12.99,
            "toppings": [self.topping_instance],
        }
        form = PizzaForm(self.request.POST)
        form.save()
        self.request.POST = {
            "name": form.instance.name,
            "cost": 5.99,
            "toppings": form.instance.toppings.all(),
        }
        form = PizzaForm(self.request.POST, instance=form.instance)
        form.save()

        self.assertTrue(form.is_valid())
        self.assertEqual(float(form.instance.cost), 5.99)

    def test_changing_instance_toppings_modifies_toppings(self):
        self.request.POST = {
            "name": "Cheese Pizza",
            "cost": 12.99,
            "toppings": [self.topping_instance],
        }
        form = PizzaForm(self.request.POST)
        form.save()
        new_topping = Topping.objects.create(name="Provolone Cheese")
        self.request.POST = {
            "name": form.instance.name,
            "cost": form.instance.cost,
            "toppings": [self.topping_instance.id, new_topping.id],
        }
        form = PizzaForm(self.request.POST, instance=form.instance)
        form.save()

        self.assertTrue(form.is_valid())


class ToppingFormTests(TestCase):
    def setUp(self):
        self.request = HttpRequest()

    def test_empty_form_contains_all_fields(self):
        form = ToppingForm()

        self.assertIn("name", form.fields)
        self.assertIn("additional_cost", form.fields)

    def test_empty_name_raises_value_error(self):
        self.request.POST = {
            "additional_cost": 0.25,
        }
        form = ToppingForm(self.request.POST)

        with self.assertRaises(ValueError):
            form.save()

    def test_duplicate_name_raises_value_error(self):
        self.request.POST = {"name": "Olives"}
        form = ToppingForm(self.request.POST)
        form.save()
        self.request.POST = {
            "name": "olives",
            "additional-cost": 0.99,
        }
        form = ToppingForm(self.request.POST)

        with self.assertRaises(ValueError):
            form.save()

    def test_empty_additional_cost_is_valid(self):
        self.request.POST = {
            "name": "Fresh Mozzarella",
        }
        form = ToppingForm(self.request.POST)

        self.assertTrue(form.is_valid())

    def test_create_new_topping(self):
        self.request.POST = {"name": "Bell Peppers"}
        form = ToppingForm(self.request.POST)

        self.assertTrue(form.is_valid())

    def test_negative_additional_cost_raises_value_error(self):
        self.request.POST = {
            "name": "Pineapple",
            "additional_cost": -1.99,
        }
        form = ToppingForm(self.request.POST)

        with self.assertRaises(ValueError):
            form.save()

    def test_changing_instance_name_modifies_name(self):
        self.request.POST = {"name": "Peproni"}
        form = ToppingForm(self.request.POST)
        form.save()
        self.request.POST = {"name": "Pepperoni"}
        form = ToppingForm(self.request.POST, instance=form.instance)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.name, "Pepperoni")

    def test_changing_instance_additional_cost_modifies_cost(self):
        self.request.POST = {"name": "Sweet Onion"}
        form = ToppingForm(self.request.POST)
        form.save()
        self.request.POST = {
            "name": form.instance.name,
            "additional_cost": 0.99,
        }
        form = ToppingForm(self.request.POST, instance=form.instance)

        self.assertTrue(form.is_valid())
        self.assertEqual(float(form.instance.additional_cost), 0.99)
