from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("portal"))

    return render(request, "home.html", {})
