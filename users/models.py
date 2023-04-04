from random import choice, randint
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


code = f'{choice(["b", "d", "e"]) + str(randint(1000, 9999)) + choice(["a", "z", "k"])}'

class ConfirmCode(models.Model):
    confirm_code = models.CharField(max_length=10, null=True, default=code)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vall_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.confirm_code, self.user.username