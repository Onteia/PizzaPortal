from django.db import models
from django.core.validators import MinValueValidator


class Topping(models.Model):
    name = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=50,
    )
    additional_cost = models.DecimalField(
        blank=True,
        null=False,
        default=0.00,
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),
        ],
    )

    def __str__(self):
        cost_text = " ($" + self.additional_cost.to_eng_string() + ")"
        return self.name + ("", cost_text)[self.additional_cost > 0]

    def delete(self, *args, **kwargs):
        parents = Pizza.objects.filter(toppings__in=[self])
        for parent in parents:
            parent.delete()
        super().delete(**kwargs)


class Pizza(models.Model):
    name = models.CharField(
        unique=True,
        max_length=100,
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=True,
        null=False,
        default="",
    )
    cost = models.DecimalField(
        blank=False,
        null=False,
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),
        ],
    )
    toppings = models.ManyToManyField(
        to=Topping,
        blank=False,
    )

    def __str__(self):
        return self.name

    def total_cost(self):
        topping_costs = 0.00
        for topping in self.toppings.filter(additional_cost__gt=0):
            topping_costs += float(topping.additional_cost)
        return float(self.cost) + topping_costs
