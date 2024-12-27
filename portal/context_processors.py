from accounts.models import AccountType
from .models import Pizza, Topping


def portal_context_processor(request):
    context = {}
    if request.user.is_authenticated:
        acct_type = request.user.account_type
        context["acct_type"] = AccountType[acct_type]
        context["items"] = (
            Topping.objects.all() if acct_type == "owner" else Pizza.objects.all()
        )

    return context
