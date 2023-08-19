from django.db import models

from account_module.models import User


# Create your models here.


class Ticket(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_view_by_admin = models.BooleanField(default=False)