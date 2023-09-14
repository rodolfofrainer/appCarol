import random, string
import factory
from . models import UserProfileModel, MarketCreatedModel, ItemCreatedModel
from django.contrib.auth.models import User

def random_password():
    length = random.randint(1, 32)
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('username')
    email = factory.Faker('email')
    password = factory.LazyFunction(random_password)

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
    user_id=factory.SubFactory(UserFactory)

class ItemCreatedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ItemCreatedModel
    
    name = factory.Faker('word')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    market_id = factory.SubFactory(MarketCreatedFactory)