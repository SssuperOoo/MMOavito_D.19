from django.db import models
from django.contrib.auth.models import User
import random

def generate_activation_code():
    return random.randint(1000, 9999)

class ActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4, unique=True, default=generate_activation_code)

    def __str__(self):
        return f'{self.user.username} - {self.code}'