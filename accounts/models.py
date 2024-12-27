from django.db import models
from django.contrib.auth.models import AbstractUser

AccountType = {
    "owner": "Owner",
    "chef": "Chef",
}


class Employee(AbstractUser):
    account_type = models.CharField(
        max_length=20, choices=AccountType, null=False, blank=False
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            return super().save(*args, **kwargs)
