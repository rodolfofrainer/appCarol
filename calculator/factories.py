import random
import string
import factory
from faker import Faker
from .models import UserProfileModel, MarketCreatedModel, ItemCreatedModel
from django.contrib.auth.models import User

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfileModel
    
    user = factory.SubFactory(UserFactory)
    wage = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    
class MarketCreatedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MarketCreatedModel
    
    name=factory.Faker('company')
    distance=factory.Faker('pyint', min_value=1, max_value=100)
    favorite=factory.Faker('boolean')
    user_id=factory.SubFactory(UserProfileFactory)

class ItemCreatedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ItemCreatedModel
    
    name = factory.Faker('word')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    market_id = factory.SubFactory(MarketCreatedFactory)