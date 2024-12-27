from django import forms
from django.core.exceptions import ValidationError
from .models import Pizza, Topping


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = "__all__"
        widgets = {"toppings": forms.CheckboxSelectMultiple}

    def clean(self):
        data = super(PizzaForm, self).clean()
        name_data = data.get("name")
        topping_data = data.get("toppings")

        case_insensitive_set = Pizza.objects.filter(name__iexact=name_data).exclude(
            pk=self.instance.pk
        )
        if case_insensitive_set.count() > 0:
            raise ValidationError("Pizza with this Name already exists.")

        if topping_data is None:
            return data

        topping_count = topping_data.count()
        partial_matches = (
            Pizza.objects.filter(toppings__in=topping_data)
            .exclude(pk=self.instance.pk)
            .distinct()
        )
        for match in partial_matches:
            if match.toppings.count() != topping_count:
                continue
            if topping_data.intersection(match.toppings.all()).count() == topping_count:
                raise ValidationError("Pizza with these Toppings already exists.")

        return data


class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = [
            "name",
            "additional_cost",
        ]

    def clean(self):
        data = super(ToppingForm, self).clean()
        name_data = data.get("name")
        case_insensitive_set = Topping.objects.filter(name__iexact=name_data).exclude(
            pk=self.instance.pk
        )

        if len(case_insensitive_set) > 0:
            raise ValidationError("Topping with this Name already exists.")

        return data
