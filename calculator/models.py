from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileModel(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    wage = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}'

class MarketCreatedModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    distance = models.IntegerField(null=True)
    favorite = models.BooleanField(null=True)
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name.title()}'

class ItemCreatedModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    market_id = models.ForeignKey(MarketCreatedModel, on_delete=models.CASCADE, related_name='items')
    
    def __str__(self):
        return f'{self.name}'