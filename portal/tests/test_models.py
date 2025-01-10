from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import Topping, Pizza


class ToppingTests(TestCase):
    def setUp(self):
        Topping.objects.create(name="Pepperoni")
        Topping.objects.create(name="Olives", additional_cost="0.99")

    def test_name_persists(self):
        pepperoni = Topping.objects.get(name="Pepperoni")

        self.assertEquals(pepperoni.name, "Pepperoni")

    def test_null_name_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Topping.objects.create(name=None)

    def test_additional_cost_persists(self):
        topping = Topping.objects.create(name="Marinara Sauce", additional_cost=1.99)
        self.assertEqual(topping.additional_cost, 1.99)

    def test_null_additional_cost_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Topping.objects.create(name="Pineapple", additional_cost=None)

    def test_topping_string_includes_cost_if_present(self):
        pepperoni_topping = Topping.objects.get(name="Pepperoni")
        olives_topping = Topping.objects.get(name="Olives")

        self.assertEqual(str(pepperoni_topping), "Pepperoni")
        self.assertEqual(str(olives_topping), "Olives ($0.99)")

    def test_deletion_removes_from_database(self):
        topping = Topping.objects.create(name="Tomato Sauce")
        topping.delete()

        with self.assertRaises(topping.DoesNotExist):
            Topping.objects.get(name="Tomato Sauce")

    def test_topping_deletion_deletes_parent_pizzas(self):
        topping = Topping.objects.create(name="Alfredo Sauce")
        pizza = Pizza.objects.create(name="White Pizza", cost=11.99)
        pizza.toppings.add(topping)
        topping.delete()

        with self.assertRaises(pizza.DoesNotExist):
            Pizza.objects.get(name="White Pizza")


class PizzaTests(TestCase):
    def setUp(self):
        self.topping_instance = Topping.objects.create(
            name="Pepperoni", additional_cost="0.25"
        )
        self.pizza_instance = Pizza.objects.create(name="Pepperoni Pizza", cost="6.99")

    def test_name_persists(self):
        self.assertEquals(self.pizza_instance.name, "Pepperoni Pizza")

    def test_null_name_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Pizza.objects.create(name=None)

    def test_description_persists(self):
        pizza = Pizza.objects.create(
            name="Descriptive Pizza", cost=12.50, description="14-inch cheese pizza"
        )

        self.assertEquals(pizza.description, "14-inch cheese pizza")

    def test_null_description_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Pizza.objects.create(name="Invalid Description", cost=11, description=None)

    def test_cost_persists(self):
        self.assertEquals(float(self.pizza_instance.cost), 6.99)

    def test_null_cost_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Pizza.objects.create(name="Invalid Pizza", cost=None)

    def test_pizza_string_returns_name(self):
        pizza = Pizza.objects.get(name="Pepperoni Pizza")

        self.assertEqual(str(pizza), "Pepperoni Pizza")

    def test_total_cost_is_sum_of_cost_and_additional_topping_costs(self):
        pizza_toppings = Topping.objects.get(name="Pepperoni")
        pizza = Pizza.objects.get(name="Pepperoni Pizza")
        pizza.toppings.add(pizza_toppings)

        self.assertEquals(pizza.total_cost(), 7.24)

    def test_deletion_removes_from_database(self):
        pizza = Pizza.objects.create(name="Neapolitan Pizza", cost=8.99)
        pizza.delete()

        with self.assertRaises(pizza.DoesNotExist):
            Pizza.objects.get(name="Neapolitan Pizza")
