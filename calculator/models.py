from .signals import create_user_profile, save_user_profile
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator


# Create your models here.
class UserProfileModel(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    wage = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    def __str__(self):
        return f'{self.user.username}'


class MarketCreatedModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    distance = models.PositiveIntegerField(null=True)
    favorite = models.BooleanField(null=True, default=False)
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name.title()}'


class ItemCreatedModel(models.Model):
    class Meta:
        ordering = ['market_id__user_id']
    name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    market_id = models.ForeignKey(
        MarketCreatedModel, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.name}'


# signals handler
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
