from django.db import models
from django.contrib.auth.models import User

class Fund(models.Model):
    scheme_code = models.CharField(max_length=20, unique=True)
    scheme_name = models.CharField(max_length=255)

    def __str__(self):
        return self.scheme_name

class SavedFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'fund')


# Create your models here.
