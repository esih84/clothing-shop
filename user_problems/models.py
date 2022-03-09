from django.db import models
from accounts.models import User


# Create your models here.

class user_problem(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='desc_question', blank=True)
    desc = models.CharField(max_length=500)
    answer = models.CharField(max_length=1000)


class profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    desc = models.TextField(blank=True)
    phone = models.CharField(max_length=11)
    postal_address = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
