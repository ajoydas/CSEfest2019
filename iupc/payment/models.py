from django.db import models

# Create your models here.
class PaymentStatus(models.Model):
    team_name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    status = models.BooleanField(default=False)


