from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .models import Pizza, Topping
from .forms import PizzaForm, ToppingForm


def portal_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy("login"))

    return render(request, "portal.html", {})


def add_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy("login"))

    acct_type = request.user.account_type
    if request.method == "POST":
        form = (
            ToppingForm(request.POST)
            if acct_type == "owner"
            else PizzaForm(request.POST)
        )

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("portal"))
    else:
        form = ToppingForm() if acct_type == "owner" else PizzaForm()
    return render(request, "add.html", {"form": form})


def edit_view(request, item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy("login"))

    acct_type = request.user.account_type
    obj = Topping if acct_type == "owner" else Pizza
    item = get_object_or_404(obj, pk=item_id)

    if request.method == "POST":
        form = (
            ToppingForm(request.POST, instance=item)
            if acct_type == "owner"
            else PizzaForm(request.POST, instance=item)
        )

        if form.is_valid():
            item = form.save(commit=False)
            form.save_m2m()
            item.save()
            return HttpResponseRedirect(reverse_lazy("portal"))
    else:
        form = (
            ToppingForm(instance=item)
            if acct_type == "owner"
            else PizzaForm(instance=item)
        )

    context = {
        "item": item,
        "form": form,
    }
    return render(request, "edit.html", context)


def delete_view(request, item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy("login"))

    if request.method == "POST":
        acct_type = request.user.account_type
        obj = Topping if acct_type == "owner" else Pizza
        item = get_object_or_404(obj, pk=item_id)

        item.delete()

    return HttpResponseRedirect(reverse_lazy("portal"))
